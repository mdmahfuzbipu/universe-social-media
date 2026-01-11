from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect

from .models import Notification


@login_required
def notifications_list(request):
    qs = request.user.notifications.select_related("sender", "post", "comment")

    # mark all unread as read
    qs.filter(read=False).update(read=True)

    notifications = qs[:50]

    return render(request, "notifications/list.html", {"notifications": notifications})


@login_required
def mark_as_read(request, notif_id):
    notif = get_object_or_404(Notification, id=notif_id, recipient=request.user)
    notif.read = True
    notif.save(update_fields=["read"])
    return redirect(request.GET.get("next", "posts:feed"))


@login_required
def delete_notification(request, notif_id):
    notif = get_object_or_404(Notification, id=notif_id, recipient=request.user)
    notif.delete()
    return redirect("notifications:list")
