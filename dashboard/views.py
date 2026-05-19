from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import date
from appointments.models import RendezVous
from doctors.models import Medecin, Specialite
from accounts.models import User
from notifications.models import Notification


@login_required
def accueil(request):
    user = request.user
    if user.is_admin():
        return redirect('dashboard:admin')
    elif user.is_medecin():
        return redirect('dashboard:medecin')
    else:
        return redirect('dashboard:patient')


@login_required
def dashboard_patient(request):
    user = request.user
    today = date.today()
    rdv_futurs = RendezVous.objects.filter(
        patient=user, date__gte=today
    ).exclude(statut=RendezVous.STATUT_ANNULE).order_by('date', 'heure')[:5]
    rdv_passes = RendezVous.objects.filter(
        patient=user, date__lt=today
    ).order_by('-date')[:5]
    rdv_annules = RendezVous.objects.filter(
        patient=user, statut=RendezVous.STATUT_ANNULE
    ).order_by('-date')[:3]
    notifications = Notification.objects.filter(utilisateur=user, est_lue=False)[:5]
    return render(request, 'dashboard/patient.html', {
        'rdv_futurs': rdv_futurs,
        'rdv_passes': rdv_passes,
        'rdv_annules': rdv_annules,
        'notifications': notifications,
    })


@login_required
def dashboard_medecin(request):
    if not request.user.is_medecin():
        return redirect('dashboard:patient')
    try:
        medecin = request.user.profil_medecin
    except Exception:
        return redirect('dashboard:patient')
    today = date.today()
    rdv_jour = RendezVous.objects.filter(
        medecin=medecin, date=today
    ).exclude(statut=RendezVous.STATUT_ANNULE).order_by('heure')
    rdv_semaine = RendezVous.objects.filter(
        medecin=medecin,
        date__gte=today,
        date__lte=today.replace(day=today.day + 6)
    ).exclude(statut=RendezVous.STATUT_ANNULE).order_by('date', 'heure')
    total_rdv = RendezVous.objects.filter(medecin=medecin).count()
    rdv_confirmes = RendezVous.objects.filter(medecin=medecin, statut=RendezVous.STATUT_CONFIRME).count()
    rdv_annules = RendezVous.objects.filter(medecin=medecin, statut=RendezVous.STATUT_ANNULE).count()
    notifications = Notification.objects.filter(utilisateur=request.user, est_lue=False)[:5]
    return render(request, 'dashboard/medecin.html', {
        'medecin': medecin,
        'rdv_jour': rdv_jour,
        'rdv_semaine': rdv_semaine,
        'total_rdv': total_rdv,
        'rdv_confirmes': rdv_confirmes,
        'rdv_annules': rdv_annules,
        'notifications': notifications,
    })


@login_required
def dashboard_admin(request):
    if not request.user.is_admin():
        return redirect('dashboard:patient')
    from django.db.models import Count
    total_patients = User.objects.filter(role='patient').count()
    total_medecins = Medecin.objects.count()
    total_rdv = RendezVous.objects.count()
    rdv_par_specialite = Specialite.objects.annotate(
        nb=Count('rendez_vous_medecin_set', distinct=True)
    )
    rdv_par_statut = {
        'attente': RendezVous.objects.filter(statut='attente').count(),
        'confirme': RendezVous.objects.filter(statut='confirme').count(),
        'annule': RendezVous.objects.filter(statut='annule').count(),
        'termine': RendezVous.objects.filter(statut='termine').count(),
    }
    from django.db.models import Count as Cnt
    medecins_top = Medecin.objects.annotate(
        nb_rdv=Cnt('rendez_vous_medecin')
    ).order_by('-nb_rdv')[:5]
    specialites_top = Specialite.objects.annotate(
        nb_rdv=Cnt('rendez_vous_medecin__rendez_vous_medecin')
    ).order_by('-nb_rdv')[:5]
    return render(request, 'dashboard/admin.html', {
        'total_patients': total_patients,
        'total_medecins': total_medecins,
        'total_rdv': total_rdv,
        'rdv_par_statut': rdv_par_statut,
        'medecins_top': medecins_top,
        'specialites_top': specialites_top,
    })
