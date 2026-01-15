from django.urls import path
from . import views

app_name = "messaging"

urlpatterns = [
    path("start/<str:username>/", views.start_conversation, name="start"),
    path("", views.inbox, name="inbox"),
    path("<int:convo_id>/", views.conversation_detail, name="detail"),
    path("<int:convo_id>/send/", views.send_message_view, name="send"),
    path("read/<int:message_id>/", views.mark_message_as_read, name="mark_as_read"),
    path("<int:convo_id>/delete/", views.delete_conversation, name="delete_conversation"),
    path("<int:convo_id>/mark-read/", views.mark_conversation_as_read, name="mark_conversation_read"),
]
