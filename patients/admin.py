from django.contrib import admin
from .models import ProfilPatient


@admin.register(ProfilPatient)
class ProfilPatientAdmin(admin.ModelAdmin):
    list_display = ['utilisateur', 'groupe_sanguin', 'mutuelle']
    search_fields = ['utilisateur__username', 'utilisateur__last_name']
