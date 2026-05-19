from django.db import models
from accounts.models import User


class ProfilPatient(models.Model):
    GROUPE_SANGUIN = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil_patient')
    adresse = models.TextField(blank=True)
    groupe_sanguin = models.CharField(max_length=5, choices=GROUPE_SANGUIN, blank=True)
    allergies = models.TextField(blank=True)
    antecedents = models.TextField(blank=True)
    mutuelle = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Profil de {self.utilisateur.get_full_name() or self.utilisateur.username}"
