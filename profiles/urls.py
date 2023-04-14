from django.urls import path
from .views import *

urlpatterns = [
    path("<slug>/", user_profile_view, name="user-profile-view"),
]
