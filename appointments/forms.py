from django import forms
from .models import RendezVous, Consultation, Avis


class RendezVousForm(forms.ModelForm):
    class Meta:
        model = RendezVous
        fields = ['date', 'heure', 'motif']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'heure': forms.TimeInput(attrs={'type': 'time'}),
            'motif': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Décrivez le motif de votre consultation...'}),
        }

    def clean_date(self):
        from datetime import date
        d = self.cleaned_data['date']
        if d < date.today():
            raise forms.ValidationError("La date doit être dans le futur.")
        return d


class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ['resume', 'diagnostic', 'traitement']
        widgets = {
            'resume': forms.Textarea(attrs={'rows': 3}),
            'diagnostic': forms.Textarea(attrs={'rows': 3}),
            'traitement': forms.Textarea(attrs={'rows': 3}),
        }


class AvisForm(forms.ModelForm):
    class Meta:
        model = Avis
        fields = ['note', 'commentaire']
        widgets = {
            'commentaire': forms.Textarea(attrs={'rows': 3}),
        }
