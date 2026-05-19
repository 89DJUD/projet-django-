from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Medecin, Specialite
from .forms import MedecinForm, RechercheForm
from schedules.models import Disponibilite


def home(request):
    specialites = Specialite.objects.all()[:6]
    medecins = Medecin.objects.filter(est_actif=True).select_related('utilisateur')[:6]
    return render(request, 'home.html', {'specialites': specialites, 'medecins': medecins})


def liste_medecins(request):
    form = RechercheForm(request.GET)
    medecins = Medecin.objects.filter(est_actif=True).select_related('utilisateur').prefetch_related('specialites')
    if form.is_valid():
        q = form.cleaned_data.get('q')
        specialite = form.cleaned_data.get('specialite')
        if q:
            medecins = medecins.filter(
                Q(utilisateur__first_name__icontains=q) |
                Q(utilisateur__last_name__icontains=q) |
                Q(specialites__nom__icontains=q)
            ).distinct()
        if specialite:
            medecins = medecins.filter(specialites=specialite)
    specialites = Specialite.objects.all()
    return render(request, 'doctors/liste.html', {
        'medecins': medecins,
        'form': form,
        'specialites': specialites,
    })


def detail_medecin(request, pk):
    medecin = get_object_or_404(Medecin, pk=pk, est_actif=True)
    disponibilites = Disponibilite.objects.filter(medecin=medecin, est_active=True)
    avis = medecin.rendez_vous_medecin.filter(
        avis__isnull=False, statut='termine'
    ).select_related('avis', 'patient')
    return render(request, 'doctors/detail.html', {
        'medecin': medecin,
        'disponibilites': disponibilites,
        'avis': avis,
    })


def liste_specialites(request):
    specialites = Specialite.objects.all()
    return render(request, 'doctors/specialites.html', {'specialites': specialites})


@login_required
def mon_profil_medecin(request):
    if not request.user.is_medecin():
        messages.error(request, "Accès réservé aux médecins.")
        return redirect('dashboard:accueil')
    medecin = get_object_or_404(Medecin, utilisateur=request.user)
    if request.method == 'POST':
        form = MedecinForm(request.POST, instance=medecin)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil médecin mis à jour.")
            return redirect('doctors:mon_profil_medecin')
    else:
        form = MedecinForm(instance=medecin)
    return render(request, 'doctors/profil_medecin.html', {'form': form, 'medecin': medecin})
