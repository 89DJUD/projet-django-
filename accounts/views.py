from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import InscriptionForm, ConnexionForm, ProfilUtilisateurForm
from .models import User


def inscription(request):
    if request.user.is_authenticated:
        return redirect('dashboard:accueil')
    if request.method == 'POST':
        form = InscriptionForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            from patients.models import ProfilPatient
            ProfilPatient.objects.create(utilisateur=user)
            login(request, user)
            messages.success(request, f"Bienvenue {user.first_name} ! Votre compte a été créé.")
            return redirect('dashboard:accueil')
    else:
        form = InscriptionForm()
    return render(request, 'accounts/inscription.html', {'form': form})


def connexion(request):
    if request.user.is_authenticated:
        return redirect('dashboard:accueil')
    if request.method == 'POST':
        form = ConnexionForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Bonjour {user.first_name or user.username} !")
            return redirect(request.GET.get('next', 'dashboard:accueil'))
        else:
            messages.error(request, "Identifiants incorrects.")
    else:
        form = ConnexionForm()
    return render(request, 'accounts/connexion.html', {'form': form})


def deconnexion(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté.")
    return redirect('home')


@login_required
def mon_profil(request):
    if request.method == 'POST':
        form = ProfilUtilisateurForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour avec succès.")
            return redirect('accounts:mon_profil')
    else:
        form = ProfilUtilisateurForm(instance=request.user)
    return render(request, 'accounts/profil.html', {'form': form})
