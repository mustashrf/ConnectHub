from django.urls import path
from .views import *

app_name = 'posts'

urlpatterns = [
    path("", main_view, name="main-view"),
    path("liked/", like_unlike_post, name="like-view"),
    path("<pk>/delete/", PostDeleteView.as_view(), name="delete-view"),
    path("<pk>/update/", PostUpdateView.as_view(), name="update-view"),
]
