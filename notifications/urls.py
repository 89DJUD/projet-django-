from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.mes_notifications, name='mes_notifications'),
    path('<int:pk>/lue/', views.marquer_lue, name='marquer_lue'),
    path('tout-lire/', views.tout_marquer_lu, name='tout_marquer_lu'),
]
