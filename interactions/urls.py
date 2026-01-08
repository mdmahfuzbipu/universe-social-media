from django.urls import path
from . import views

app_name = "interactions"

urlpatterns = [
    path("follow/<str:username>/", views.follow_toggle, name="follow_toggle"),
    path("react/<int:post_id>/", views.reaction_toggle, name="reaction_toggle"),
]
