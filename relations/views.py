from django.db.models import Q
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .services import (accept_friendship_invitation, delete_friendship_invitation,
                       list_friendship_invitations, send_friendship_invitation)
from .exeptions import ServiceException
from .serializers import UserFriendInvitationsSerializer

from users.models import User

# Create your views here.


class FriendshipInvitationApiView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserFriendInvitationsSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = User.friend_invitations.through.objects.filter(Q(from_user_id=user) | Q(to_user_id=user))
        return queryset

    def get(self, request: Request) -> Response:
        """List all friendship invitations sent to current user"""

        friendship_invitations = list_friendship_invitations(user=request.user, queryset=self.get_queryset())
        serializer = self.serializer_class(friendship_invitations, many=True)
        return Response(serializer.data)

    def post(self, request: Request, friend_id: int) -> Response:
        """Send a friendship invitation to user"""

        try:
            friendship_invitation = send_friendship_invitation(user=request.user, friend_id=friend_id)
            return Response(friendship_invitation, status=status.HTTP_201_CREATED)
        except ServiceException as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, friend_id: int) -> Response:
        """Delete or reject friendship invitation"""

        try:
            rejected_invitation = delete_friendship_invitation(user=request.user,
                                                               friend_id=friend_id,
                                                               queryset=self.get_queryset())
            return Response(rejected_invitation, status=status.HTTP_204_NO_CONTENT)
        except ServiceException as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def put(self, request: Request, friend_id: int) -> Response:
        """Accept friendship invitation and add to friends list"""

        try:
            accepted_invitation = accept_friendship_invitation(user=request.user,
                                                               friend_id=friend_id,
                                                               queryset=self.get_queryset())
            return Response(accepted_invitation, status=status.HTTP_204_NO_CONTENT)
        except ServiceException as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class FriendshipRelationApiView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        pass

    def get(self):
        """List all friends"""

    def delete(self):
        """Delete user from friends"""


class BlockApiView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        pass

    def get(self):
        """List all blocked relations"""

    def post(self):
        """Block users"""

    def put(self):
        """Unblock users"""


