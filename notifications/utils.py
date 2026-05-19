from .models import Notification


def creer_notification(utilisateur, titre, message, type_notif='info', lien=''):
    Notification.objects.create(
        utilisateur=utilisateur,
        titre=titre,
        message=message,
        type_notif=type_notif,
        lien=lien,
    )
