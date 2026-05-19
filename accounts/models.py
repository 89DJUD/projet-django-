from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_PATIENT = 'patient'
    ROLE_MEDECIN = 'medecin'
    ROLE_ADMIN = 'admin'

    ROLES = [
        (ROLE_PATIENT, 'Patient'),
        (ROLE_MEDECIN, 'Médecin'),
        (ROLE_ADMIN, 'Administrateur'),
    ]

    role = models.CharField(max_length=10, choices=ROLES, default=ROLE_PATIENT)
    telephone = models.CharField(max_length=20, blank=True)
    photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    date_naissance = models.DateField(blank=True, null=True)

    def is_patient(self):
        return self.role == self.ROLE_PATIENT

    def is_medecin(self):
        return self.role == self.ROLE_MEDECIN

    def is_admin(self):
        return self.role == self.ROLE_ADMIN or self.is_superuser

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"
