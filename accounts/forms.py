from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class InscriptionForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True, label="Prénom")
    last_name = forms.CharField(max_length=50, required=True, label="Nom")
    email = forms.EmailField(required=True, label="Email")
    telephone = forms.CharField(max_length=20, required=False, label="Téléphone")
    date_naissance = forms.DateField(
        required=False,
        label="Date de naissance",
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'telephone',
                  'date_naissance', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.ROLE_PATIENT
        if commit:
            user.save()
        return user


class ConnexionForm(AuthenticationForm):
    username = forms.CharField(label="Nom d'utilisateur ou Email")


class ProfilUtilisateurForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'telephone', 'date_naissance', 'photo']
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
        }
