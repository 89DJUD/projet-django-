from django.urls import path
from . import views

app_name = 'schedules'

urlpatterns = [
    path('', views.mes_disponibilites, name='mes_disponibilites'),
    path('ajouter/', views.ajouter_disponibilite, name='ajouter_disponibilite'),
    path('<int:pk>/supprimer/', views.supprimer_disponibilite, name='supprimer_disponibilite'),
    path('indisponibilite/ajouter/', views.ajouter_indisponibilite, name='ajouter_indisponibilite'),
]
