from django.db import models
from django.utils import timezone
from accounts.models import User


class Notification(models.Model):
    TYPE_INFO = 'info'
    TYPE_SUCCES = 'succes'
    TYPE_ALERTE = 'alerte'
    TYPE_ERREUR = 'erreur'

    TYPES = [
        (TYPE_INFO, 'Information'),
        (TYPE_SUCCES, 'Succès'),
        (TYPE_ALERTE, 'Alerte'),
        (TYPE_ERREUR, 'Erreur'),
    ]

    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    titre = models.CharField(max_length=200)
    message = models.TextField()
    type_notif = models.CharField(max_length=10, choices=TYPES, default=TYPE_INFO)
    est_lue = models.BooleanField(default=False)
    date_creation = models.DateTimeField(default=timezone.now)
    lien = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = "Notification"
        ordering = ['-date_creation']

    def __str__(self):
        return f"[{self.type_notif}] {self.titre} -> {self.utilisateur}"
