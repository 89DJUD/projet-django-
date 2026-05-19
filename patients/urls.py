from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    path('profil/', views.mon_profil, name='mon_profil'),
]
