from django.shortcuts import render
from .engine import recommander_specialite
from doctors.models import Specialite, Medecin


def orientation(request):
    resultats = []
    motif = ''
    medecins_suggeres = []
    if request.method == 'POST':
        motif = request.POST.get('motif', '').strip()
        if motif:
            resultats = recommander_specialite(motif)
            if resultats:
                specialite_nom = resultats[0]['specialite']
                try:
                    specialite = Specialite.objects.get(nom__icontains=specialite_nom.split()[0])
                    medecins_suggeres = Medecin.objects.filter(
                        specialites=specialite, est_actif=True
                    ).select_related('utilisateur')[:3]
                except Specialite.DoesNotExist:
                    medecins_suggeres = Medecin.objects.filter(est_actif=True)[:3]
    return render(request, 'ai_orientation/orientation.html', {
        'motif': motif,
        'resultats': resultats,
        'medecins_suggeres': medecins_suggeres,
    })
