from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ProfilPatient
from .forms import ProfilPatientForm
from accounts.forms import ProfilUtilisateurForm


@login_required
def mon_profil(request):
    if not request.user.is_patient():
        return redirect('dashboard:accueil')
    profil, _ = ProfilPatient.objects.get_or_create(utilisateur=request.user)
    if request.method == 'POST':
        user_form = ProfilUtilisateurForm(request.POST, request.FILES, instance=request.user)
        profil_form = ProfilPatientForm(request.POST, instance=profil)
        if user_form.is_valid() and profil_form.is_valid():
            user_form.save()
            profil_form.save()
            messages.success(request, "Profil mis à jour.")
            return redirect('patients:mon_profil')
    else:
        user_form = ProfilUtilisateurForm(instance=request.user)
        profil_form = ProfilPatientForm(instance=profil)
    return render(request, 'patients/profil.html', {
        'user_form': user_form,
        'profil_form': profil_form,
    })
