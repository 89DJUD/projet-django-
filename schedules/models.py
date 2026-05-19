from django.db import models
from doctors.models import Medecin


JOURS_SEMAINE = [
    (0, 'Lundi'), (1, 'Mardi'), (2, 'Mercredi'),
    (3, 'Jeudi'), (4, 'Vendredi'), (5, 'Samedi'), (6, 'Dimanche'),
]


class Disponibilite(models.Model):
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE, related_name='disponibilites')
    jour = models.IntegerField(choices=JOURS_SEMAINE)
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    duree_rdv = models.IntegerField(default=30, help_text="Durée en minutes")
    est_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Disponibilité"
        ordering = ['jour', 'heure_debut']
        unique_together = ['medecin', 'jour', 'heure_debut']

    def __str__(self):
        return f"{self.medecin} - {self.get_jour_display()} {self.heure_debut}-{self.heure_fin}"


class Indisponibilite(models.Model):
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE, related_name='indisponibilites')
    date_debut = models.DateField()
    date_fin = models.DateField()
    motif = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = "Indisponibilité"

    def __str__(self):
        return f"{self.medecin} indisponible du {self.date_debut} au {self.date_fin}"
