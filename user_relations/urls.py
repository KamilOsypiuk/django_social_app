from django.urls import path

from .views import FriendshipRequestApiView

urlpatterns = [
    path(
        "friend-requests/", FriendshipRequestApiView.as_view(), name="friend-requests"
    ),
    path(
        "friend-requests/<int:request_id>/accept/",
        FriendshipRequestApiView.as_view(),
        name="accept-friend-request",
    ),
    path(
        "friend-request/<int:request_id>/delete/",
        FriendshipRequestApiView.as_view(),
        name="delete-friend-request",
    ),
]
