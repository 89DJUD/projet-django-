from django.contrib import admin
from .models import RendezVous, Consultation, Avis


@admin.register(RendezVous)
class RendezVousAdmin(admin.ModelAdmin):
    list_display = ['patient', 'medecin', 'date', 'heure', 'statut', 'specialite']
    list_filter = ['statut', 'date', 'specialite']
    search_fields = ['patient__username', 'medecin__utilisateur__last_name']
    date_hierarchy = 'date'


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ['rendez_vous', 'date_creation']


@admin.register(Avis)
class AvisAdmin(admin.ModelAdmin):
    list_display = ['rendez_vous', 'note', 'date_creation']
    list_filter = ['note']
