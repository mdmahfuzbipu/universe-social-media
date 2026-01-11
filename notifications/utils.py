from .models import Notification


def create_notification(recipient, sender, notif_type, post=None, comment=None):
    # Avoid sending notifications to yourself
    if recipient == sender:
        return None
    return Notification.objects.create(
        recipient=recipient,
        sender=sender,
        notif_type=notif_type,
        post=post,
        comment=comment,
    )
