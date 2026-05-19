from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta, date
from .models import RendezVous, Consultation, Avis
from .forms import RendezVousForm, ConsultationForm, AvisForm
from doctors.models import Medecin
from notifications.utils import creer_notification


def _creneaux_disponibles(medecin, date_rdv):
    from schedules.models import Disponibilite, Indisponibilite
    jour = date_rdv.weekday()
    dispos = Disponibilite.objects.filter(medecin=medecin, jour=jour, est_active=True)
    indispos = Indisponibilite.objects.filter(
        medecin=medecin, date_debut__lte=date_rdv, date_fin__gte=date_rdv
    )
    if indispos.exists():
        return []
    rdv_pris = RendezVous.objects.filter(
        medecin=medecin, date=date_rdv
    ).exclude(statut=RendezVous.STATUT_ANNULE).values_list('heure', flat=True)
    creneaux = []
    for dispo in dispos:
        current = datetime.combine(date_rdv, dispo.heure_debut)
        end = datetime.combine(date_rdv, dispo.heure_fin)
        while current + timedelta(minutes=dispo.duree_rdv) <= end:
            if current.time() not in rdv_pris:
                creneaux.append(current.time())
            current += timedelta(minutes=dispo.duree_rdv)
    return creneaux


@login_required
def prendre_rdv(request, medecin_pk):
    if not request.user.is_patient():
        messages.error(request, "Seuls les patients peuvent prendre rendez-vous.")
        return redirect('doctors:liste')
    medecin = get_object_or_404(Medecin, pk=medecin_pk, est_actif=True)
    creneaux = []
    date_choisie = None
    if request.method == 'GET' and request.GET.get('date'):
        try:
            date_choisie = datetime.strptime(request.GET['date'], '%Y-%m-%d').date()
            if date_choisie >= date.today():
                creneaux = _creneaux_disponibles(medecin, date_choisie)
        except ValueError:
            pass
    if request.method == 'POST':
        form = RendezVousForm(request.POST)
        if form.is_valid():
            rdv_date = form.cleaned_data['date']
            rdv_heure = form.cleaned_data['heure']
            conflit = RendezVous.objects.filter(
                medecin=medecin, date=rdv_date, heure=rdv_heure
            ).exclude(statut=RendezVous.STATUT_ANNULE).exists()
            if conflit:
                messages.error(request, "Ce créneau n'est plus disponible. Choisissez un autre.")
            else:
                specialite = medecin.specialites.first()
                rdv = form.save(commit=False)
                rdv.patient = request.user
                rdv.medecin = medecin
                rdv.specialite = specialite
                rdv.save()
                creer_notification(
                    request.user,
                    "Rendez-vous créé",
                    f"Votre RDV avec {medecin} le {rdv_date} à {rdv_heure} est en attente de confirmation.",
                    'succes'
                )
                creer_notification(
                    medecin.utilisateur,
                    "Nouveau rendez-vous",
                    f"Nouveau RDV de {request.user.get_full_name()} le {rdv_date} à {rdv_heure}.",
                    'info'
                )
                messages.success(request, "Rendez-vous créé avec succès !")
                return redirect('appointments:mes_rdv')
    else:
        form = RendezVousForm()
    return render(request, 'appointments/prendre_rdv.html', {
        'medecin': medecin,
        'form': form,
        'creneaux': creneaux,
        'date_choisie': date_choisie,
    })


@login_required
def mes_rdv(request):
    user = request.user
    if user.is_patient():
        rdv_futurs = RendezVous.objects.filter(
            patient=user, date__gte=date.today()
        ).exclude(statut=RendezVous.STATUT_ANNULE).order_by('date', 'heure')
        rdv_passes = RendezVous.objects.filter(
            patient=user, date__lt=date.today()
        ).order_by('-date', '-heure')
        rdv_annules = RendezVous.objects.filter(
            patient=user, statut=RendezVous.STATUT_ANNULE
        ).order_by('-date')
    else:
        rdv_futurs = rdv_passes = rdv_annules = []
    return render(request, 'appointments/mes_rdv.html', {
        'rdv_futurs': rdv_futurs,
        'rdv_passes': rdv_passes,
        'rdv_annules': rdv_annules,
    })


@login_required
def annuler_rdv(request, pk):
    rdv = get_object_or_404(RendezVous, pk=pk)
    if request.user != rdv.patient and not request.user.is_medecin():
        messages.error(request, "Vous n'êtes pas autorisé à annuler ce rendez-vous.")
        return redirect('appointments:mes_rdv')
    if not rdv.peut_annuler():
        messages.error(request, "Ce rendez-vous ne peut plus être annulé.")
        return redirect('appointments:mes_rdv')
    if request.method == 'POST':
        rdv.statut = RendezVous.STATUT_ANNULE
        rdv.save()
        creer_notification(rdv.patient, "Rendez-vous annulé",
                           f"Votre RDV du {rdv.date} à {rdv.heure} a été annulé.", 'alerte')
        messages.success(request, "Rendez-vous annulé.")
        return redirect('appointments:mes_rdv')
    return render(request, 'appointments/confirmer_annulation.html', {'rdv': rdv})


@login_required
def confirmer_rdv(request, pk):
    if not request.user.is_medecin():
        return redirect('dashboard:accueil')
    rdv = get_object_or_404(RendezVous, pk=pk, medecin__utilisateur=request.user)
    rdv.statut = RendezVous.STATUT_CONFIRME
    rdv.save()
    creer_notification(rdv.patient, "Rendez-vous confirmé",
                       f"Votre RDV du {rdv.date} à {rdv.heure} avec {rdv.medecin} est confirmé.", 'succes')
    messages.success(request, "Rendez-vous confirmé.")
    return redirect('dashboard:accueil')


@login_required
def ajouter_consultation(request, rdv_pk):
    if not request.user.is_medecin():
        return redirect('dashboard:accueil')
    rdv = get_object_or_404(RendezVous, pk=rdv_pk, medecin__utilisateur=request.user)
    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        if form.is_valid():
            consultation = form.save(commit=False)
            consultation.rendez_vous = rdv
            consultation.save()
            rdv.statut = RendezVous.STATUT_TERMINE
            rdv.save()
            messages.success(request, "Compte-rendu de consultation enregistré.")
            return redirect('dashboard:accueil')
    else:
        form = ConsultationForm()
    return render(request, 'appointments/consultation.html', {'form': form, 'rdv': rdv})


@login_required
def donner_avis(request, rdv_pk):
    if not request.user.is_patient():
        return redirect('dashboard:accueil')
    rdv = get_object_or_404(RendezVous, pk=rdv_pk, patient=request.user, statut=RendezVous.STATUT_TERMINE)
    if hasattr(rdv, 'avis'):
        messages.info(request, "Vous avez déjà donné un avis pour ce rendez-vous.")
        return redirect('appointments:mes_rdv')
    if request.method == 'POST':
        form = AvisForm(request.POST)
        if form.is_valid():
            avis = form.save(commit=False)
            avis.rendez_vous = rdv
            avis.save()
            messages.success(request, "Merci pour votre avis !")
            return redirect('appointments:mes_rdv')
    else:
        form = AvisForm()
    return render(request, 'appointments/avis.html', {'form': form, 'rdv': rdv})
