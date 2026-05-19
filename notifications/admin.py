from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['utilisateur', 'titre', 'type_notif', 'est_lue', 'date_creation']
    list_filter = ['type_notif', 'est_lue']
    search_fields = ['utilisateur__username', 'titre']
