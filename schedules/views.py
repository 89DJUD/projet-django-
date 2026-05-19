from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Disponibilite, Indisponibilite
from .forms import DisponibiliteForm, IndisponibiliteForm
from doctors.models import Medecin


@login_required
def mes_disponibilites(request):
    if not request.user.is_medecin():
        messages.error(request, "Accès réservé aux médecins.")
        return redirect('dashboard:accueil')
    medecin = get_object_or_404(Medecin, utilisateur=request.user)
    disponibilites = Disponibilite.objects.filter(medecin=medecin).order_by('jour', 'heure_debut')
    indisponibilites = Indisponibilite.objects.filter(medecin=medecin).order_by('date_debut')
    return render(request, 'schedules/disponibilites.html', {
        'disponibilites': disponibilites,
        'indisponibilites': indisponibilites,
        'medecin': medecin,
    })


@login_required
def ajouter_disponibilite(request):
    if not request.user.is_medecin():
        return redirect('dashboard:accueil')
    medecin = get_object_or_404(Medecin, utilisateur=request.user)
    if request.method == 'POST':
        form = DisponibiliteForm(request.POST)
        if form.is_valid():
            dispo = form.save(commit=False)
            dispo.medecin = medecin
            dispo.save()
            messages.success(request, "Disponibilité ajoutée.")
            return redirect('schedules:mes_disponibilites')
    else:
        form = DisponibiliteForm()
    return render(request, 'schedules/form_disponibilite.html', {'form': form})


@login_required
def supprimer_disponibilite(request, pk):
    if not request.user.is_medecin():
        return redirect('dashboard:accueil')
    medecin = get_object_or_404(Medecin, utilisateur=request.user)
    dispo = get_object_or_404(Disponibilite, pk=pk, medecin=medecin)
    dispo.delete()
    messages.success(request, "Disponibilité supprimée.")
    return redirect('schedules:mes_disponibilites')


@login_required
def ajouter_indisponibilite(request):
    if not request.user.is_medecin():
        return redirect('dashboard:accueil')
    medecin = get_object_or_404(Medecin, utilisateur=request.user)
    if request.method == 'POST':
        form = IndisponibiliteForm(request.POST)
        if form.is_valid():
            indispo = form.save(commit=False)
            indispo.medecin = medecin
            indispo.save()
            messages.success(request, "Période d'indisponibilité ajoutée.")
            return redirect('schedules:mes_disponibilites')
    else:
        form = IndisponibiliteForm()
    return render(request, 'schedules/form_indisponibilite.html', {'form': form})
