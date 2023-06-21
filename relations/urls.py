from django.urls import path

from .views import FriendshipInvitationApiView

urlpatterns = [
    path(
        "friend-invitation/", FriendshipInvitationApiView.as_view(), name="friend-invitation"
    ),
    path(
        "friend-invitation/<int:friend_id>/send/",
        FriendshipInvitationApiView.as_view(),
        name="send-friend-invitation",
    ),
    path(
        "friend-invitation/<int:friend_id>/accept/",
        FriendshipInvitationApiView.as_view(),
        name="accept-friend-invitation",
    ),
    path(
        "friend-invitation/<int:friend_id>/delete/",
        FriendshipInvitationApiView.as_view(),
        name="delete-friend-invitation",
    ),
]
