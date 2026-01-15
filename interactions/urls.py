from django.urls import path
from . import views

app_name = "interactions"

urlpatterns = [
    path("follow/<str:username>/", views.follow_toggle, name="follow_toggle"),
    path("react/<int:post_id>/", views.reaction_toggle, name="reaction_toggle"),
    path("comment/<int:post_id>/", views.add_comment, name="add_comment"),
    path("comment/<int:comment_id>/edit/", views.edit_comment, name="edit_comment"),
    path(
        "comment/<int:comment_id>/delete/", views.delete_comment, name="delete_comment"
    ),
]
