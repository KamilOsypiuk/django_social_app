from django.db.models import Q
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .services import (accept_friendship_invitation, delete_friendship_invitation,
                       send_friendship_invitation, delete_friend, block_user, unblock_user)
from .exeptions import ServiceException
from .serializers import UserFriendInvitationsSerializer, UserFriendsSerializer, UserBlocksSerializer

from users.models import User

# Create your views here.


class FriendshipInvitationApiView(GenericAPIView, ListModelMixin):
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserFriendInvitationsSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = User.friend_invitations.through.objects.filter(Q(from_user_id=user) |
                                                                  Q(to_user_id=user)).order_by('id')
        return queryset

    def get(self, request: Request) -> Response:
        """List all friendship invitations sent to current user"""

        return self.list(request=request)

    def post(self, request: Request, friend_id: int) -> Response:
        """Send a friendship invitation to user"""

        try:
            friendship_invitation = send_friendship_invitation(user=request.user, friend_id=friend_id)
            return Response(friendship_invitation, status=status.HTTP_201_CREATED)
        except ServiceException as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, invitation_id: int) -> Response:
        """Delete or reject friendship invitation"""

        rejected_invitation = delete_friendship_invitation(user=request.user, invitation_id=invitation_id,
                                                           queryset=self.get_queryset())
        return Response(rejected_invitation, status=status.HTTP_200_OK)

    def put(self, request: Request, invitation_id: int) -> Response:
        """Accept friendship invitation and add to friends list"""

        try:
            accepted_invitation = accept_friendship_invitation(user=request.user, invitation_id=invitation_id,
                                                               queryset=self.get_queryset())
            return Response(accepted_invitation, status=status.HTTP_200_OK)
        except ServiceException as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class FriendshipRelationApiView(GenericAPIView, ListModelMixin):
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserFriendsSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = User.friends.through.objects.filter(from_user_id=user).order_by('id')
        return queryset

    def get(self, request: Request) -> Response:
        """List all friends"""

        return self.list(request=request)

    def delete(self, request: Request, relation_id: int) -> Response:
        """Remove user from friends"""

        removed_friend = delete_friend(user=request.user, relation_id=relation_id, queryset=self.get_queryset())
        return Response(removed_friend, status=status.HTTP_200_OK)


class BlockApiView(GenericAPIView, ListModelMixin):
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserBlocksSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = User.blocks.through.objects.filter(Q(from_user_id=user.pk) | Q(to_user_id=user.pk)).order_by('id')
        return queryset

    def get(self, request: Request) -> Response:
        """List all blocked relations"""

        return self.list(request=request)

    def post(self, request: Request, user_id: int) -> Response:
        """Block users"""

        try:
            blocked_relation = block_user(user=request.user, user_id=user_id)
            return Response(blocked_relation, status=status.HTTP_201_CREATED)
        except ServiceException as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, block_id: int):
        """Unblock users"""

        try:
            unblocked_relation = unblock_user(user=request.user, block_id=block_id, queryset=self.get_queryset())
            return Response(unblocked_relation, status=status.HTTP_200_OK)
        except ServiceException as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

