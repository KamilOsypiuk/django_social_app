from django.urls import path

from .views import FriendshipInvitationApiView, BlockApiView, FriendshipRelationApiView

urlpatterns = [
    path(
        "friend-invitations/", FriendshipInvitationApiView.as_view(), name="friend-invitation-list"
    ),
    path(
        "friend-invitations/<int:friend_id>/send/", FriendshipInvitationApiView.as_view(),
        name="friend-invitation-send",
    ),
    path(
        "friend-invitations/<int:invitation_id>/accept/", FriendshipInvitationApiView.as_view(),
        name='friend-invitation-accept',
    ),
    path(
        "friend-invitations/<int:invitation_id>/delete/", FriendshipInvitationApiView.as_view(),
        name="friend-invitation-delete",
    ),
    path(
        "friends/", FriendshipRelationApiView.as_view(), name="friend-list",
    ),
    path(
        "friends/<int:relation_id>/delete", FriendshipRelationApiView.as_view(), name='friend-delete',
    ),
    path(
        "blocked/", BlockApiView.as_view(), name='blocked-users-list'
    ),
    path(
        "users/<int:user_id>/block", BlockApiView.as_view(), name='block-user'
    ),
    path(
        "users/<int:block_id>/unblock", BlockApiView.as_view(), name='unblock-user'
    ),
]
