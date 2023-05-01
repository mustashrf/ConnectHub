from django.urls import path
from .views import *

app_name = 'profiles'

urlpatterns = [
    path("", ProfileListView.as_view(), name="profiles-list-view"),
    path("me/", user_profile_view, name="my-profile-view"),
    path("invitations/", received_invitations_view, name="invitations-view"),
    path("available/", available_invitations_view, name="available-invitations-view"),
    path("send-invitation/", send_invitation, name="send-invitation"),
    path("add-friend/", add_friend, name="add-friend"),
    path("remove-friend/", remove_friend, name="remove-friend"),
    path("reject-invitation/", reject_invitation, name="reject-invitation"),
    path("ignore-invitation/", ignore_invitation, name="ignore-invitation"),
    path("<slug>/", ProfileDetailView.as_view(), name="user-profile-view"),
]
