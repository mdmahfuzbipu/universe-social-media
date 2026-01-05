from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path("feed/", views.feed, name="feed"),
    path("create/", views.create_post, name="create_post"),
    path("<int:post_id>/edit/", views.edit_post, name="edit_post"),
    path("<int:post_id>/delete/", views.delete_post, name="delete_post"),
    path("share/<int:post_id>/", views.share_post, name="share_post"),
]
