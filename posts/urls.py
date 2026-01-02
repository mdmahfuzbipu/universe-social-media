from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path("feed/", views.feed, name="feed"),
    path("create/", views.create_post, name="create_post"),
]
