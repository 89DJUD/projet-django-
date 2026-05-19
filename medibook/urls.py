from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('doctors.urls')),
    path('accounts/', include('accounts.urls')),
    path('patients/', include('patients.urls')),
    path('medecins/', include(('doctors.urls_doctors', 'doctors_mgmt'), namespace='doctors_mgmt')),
    path('rendez-vous/', include('appointments.urls')),
    path('planning/', include('schedules.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('orientation/', include('ai_orientation.urls')),
    path('notifications/', include('notifications.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
