from django.contrib import admin
from .models import Disponibilite, Indisponibilite


@admin.register(Disponibilite)
class DisponibiliteAdmin(admin.ModelAdmin):
    list_display = ['medecin', 'get_jour_display', 'heure_debut', 'heure_fin', 'duree_rdv', 'est_active']
    list_filter = ['jour', 'est_active']


@admin.register(Indisponibilite)
class IndisponibiliteAdmin(admin.ModelAdmin):
    list_display = ['medecin', 'date_debut', 'date_fin', 'motif']
