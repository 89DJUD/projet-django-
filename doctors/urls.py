from django.urls import path
from . import views

app_name = 'doctors'

urlpatterns = [
    path('', views.home, name='home'),
    path('medecins/', views.liste_medecins, name='liste'),
    path('medecins/<int:pk>/', views.detail_medecin, name='detail'),
    path('specialites/', views.liste_specialites, name='specialites'),
]
