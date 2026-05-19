from django.db import models
from accounts.models import User


class Specialite(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icone = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = "Spécialité"
        ordering = ['nom']

    def __str__(self):
        return self.nom


class Medecin(models.Model):
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil_medecin')
    specialites = models.ManyToManyField(Specialite, related_name='medecins')
    telephone_pro = models.CharField(max_length=20)
    adresse_cabinet = models.TextField()
    description = models.TextField(blank=True)
    annees_experience = models.PositiveIntegerField(default=0)
    numero_ordre = models.CharField(max_length=50, blank=True)
    est_actif = models.BooleanField(default=True)
    tarif_consultation = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Médecin"
        ordering = ['utilisateur__last_name']

    def __str__(self):
        return f"Dr. {self.utilisateur.get_full_name() or self.utilisateur.username}"

    def specialites_liste(self):
        return ", ".join(s.nom for s in self.specialites.all())
