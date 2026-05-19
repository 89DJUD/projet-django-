from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('patient/', views.dashboard_patient, name='patient'),
    path('medecin/', views.dashboard_medecin, name='medecin'),
    path('admin/', views.dashboard_admin, name='admin'),
]
