from django.db import models
from django.utils import timezone
from accounts.models import User
from doctors.models import Medecin, Specialite


class RendezVous(models.Model):
    STATUT_ATTENTE = 'attente'
    STATUT_CONFIRME = 'confirme'
    STATUT_ANNULE = 'annule'
    STATUT_TERMINE = 'termine'
    STATUT_ABSENT = 'absent'

    STATUTS = [
        (STATUT_ATTENTE, 'En attente'),
        (STATUT_CONFIRME, 'Confirmé'),
        (STATUT_ANNULE, 'Annulé'),
        (STATUT_TERMINE, 'Terminé'),
        (STATUT_ABSENT, 'Absent'),
    ]

    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rendez_vous_patient')
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE, related_name='rendez_vous_medecin')
    specialite = models.ForeignKey(Specialite, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    heure = models.TimeField()
    motif = models.TextField()
    statut = models.CharField(max_length=10, choices=STATUTS, default=STATUT_ATTENTE)
    date_creation = models.DateTimeField(default=timezone.now)
    notes_medecin = models.TextField(blank=True)

    class Meta:
        verbose_name = "Rendez-vous"
        verbose_name_plural = "Rendez-vous"
        ordering = ['-date', '-heure']

    def __str__(self):
        return f"RDV {self.patient} avec {self.medecin} le {self.date} à {self.heure}"

    def est_futur(self):
        from datetime import datetime, date
        today = date.today()
        return self.date > today or (self.date == today and self.heure > datetime.now().time())

    def peut_annuler(self):
        return self.statut in [self.STATUT_ATTENTE, self.STATUT_CONFIRME] and self.est_futur()


class Consultation(models.Model):
    rendez_vous = models.OneToOneField(RendezVous, on_delete=models.CASCADE, related_name='consultation')
    resume = models.TextField()
    diagnostic = models.TextField(blank=True)
    traitement = models.TextField(blank=True)
    date_creation = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Consultation"

    def __str__(self):
        return f"Consultation de {self.rendez_vous}"


class Avis(models.Model):
    NOTE_CHOICES = [(i, str(i)) for i in range(1, 6)]

    rendez_vous = models.OneToOneField(RendezVous, on_delete=models.CASCADE, related_name='avis')
    note = models.IntegerField(choices=NOTE_CHOICES)
    commentaire = models.TextField(blank=True)
    date_creation = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Avis"
        verbose_name_plural = "Avis"

    def __str__(self):
        return f"Avis {self.note}/5 pour {self.rendez_vous}"
