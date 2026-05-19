from django.contrib import admin
from .models import Specialite, Medecin


@admin.register(Specialite)
class SpecialiteAdmin(admin.ModelAdmin):
    list_display = ['nom']
    search_fields = ['nom']


@admin.register(Medecin)
class MedecinAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'specialites_liste', 'telephone_pro', 'est_actif']
    list_filter = ['est_actif', 'specialites']
    search_fields = ['utilisateur__first_name', 'utilisateur__last_name']
    filter_horizontal = ['specialites']
