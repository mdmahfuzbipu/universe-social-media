from django.urls import path
from . import views

app_name = "notifications"

urlpatterns = [
    path("", views.notifications_list, name="list"),
    path("read/<int:notif_id>/", views.mark_as_read, name="mark_as_read"),
    path("delete/<int:notif_id>/", views.delete_notification, name="delete"),
]
