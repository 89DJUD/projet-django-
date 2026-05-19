from django import forms
from .models import Disponibilite, Indisponibilite


class DisponibiliteForm(forms.ModelForm):
    class Meta:
        model = Disponibilite
        fields = ['jour', 'heure_debut', 'heure_fin', 'duree_rdv', 'est_active']
        widgets = {
            'heure_debut': forms.TimeInput(attrs={'type': 'time'}),
            'heure_fin': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        cleaned = super().clean()
        debut = cleaned.get('heure_debut')
        fin = cleaned.get('heure_fin')
        if debut and fin and debut >= fin:
            raise forms.ValidationError("L'heure de fin doit être après l'heure de début.")
        return cleaned


class IndisponibiliteForm(forms.ModelForm):
    class Meta:
        model = Indisponibilite
        fields = ['date_debut', 'date_fin', 'motif']
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
        }
