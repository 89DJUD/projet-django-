from django import forms
from .models import ProfilPatient


class ProfilPatientForm(forms.ModelForm):
    class Meta:
        model = ProfilPatient
        fields = ['adresse', 'groupe_sanguin', 'allergies', 'antecedents', 'mutuelle']
        widgets = {
            'adresse': forms.Textarea(attrs={'rows': 2}),
            'allergies': forms.Textarea(attrs={'rows': 2}),
            'antecedents': forms.Textarea(attrs={'rows': 2}),
        }
