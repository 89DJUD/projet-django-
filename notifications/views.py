from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification


@login_required
def mes_notifications(request):
    notifications = Notification.objects.filter(utilisateur=request.user).order_by('-date_creation')
    return render(request, 'notifications/liste.html', {'notifications': notifications})


@login_required
def marquer_lue(request, pk):
    notif = get_object_or_404(Notification, pk=pk, utilisateur=request.user)
    notif.est_lue = True
    notif.save()
    return redirect('notifications:mes_notifications')


@login_required
def tout_marquer_lu(request):
    Notification.objects.filter(utilisateur=request.user, est_lue=False).update(est_lue=True)
    return redirect('notifications:mes_notifications')
