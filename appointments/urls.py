from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('', views.mes_rdv, name='mes_rdv'),
    path('prendre/<int:medecin_pk>/', views.prendre_rdv, name='prendre_rdv'),
    path('<int:pk>/annuler/', views.annuler_rdv, name='annuler_rdv'),
    path('<int:pk>/confirmer/', views.confirmer_rdv, name='confirmer_rdv'),
    path('<int:rdv_pk>/consultation/', views.ajouter_consultation, name='consultation'),
    path('<int:rdv_pk>/avis/', views.donner_avis, name='avis'),
]
