from django import forms
from .models import Medecin, Specialite


class MedecinForm(forms.ModelForm):
    class Meta:
        model = Medecin
        fields = ['specialites', 'telephone_pro', 'adresse_cabinet', 'description',
                  'annees_experience', 'numero_ordre', 'tarif_consultation']
        widgets = {
            'specialites': forms.CheckboxSelectMultiple(),
            'adresse_cabinet': forms.Textarea(attrs={'rows': 2}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class RechercheForm(forms.Form):
    q = forms.CharField(required=False, label="Recherche", max_length=100,
                        widget=forms.TextInput(attrs={'placeholder': 'Nom, spécialité...'}))
    specialite = forms.ModelChoiceField(
        queryset=Specialite.objects.all(),
        required=False,
        label="Spécialité",
        empty_label="Toutes les spécialités"
    )
