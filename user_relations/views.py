from django.core.exceptions import BadRequest
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import FriendshipRequestSerializer
from .services import (accept_friendship_request, delete_friendship_request,
                       list_friendship_requests, send_friendship_request)

# Create your views here.


class FriendshipRequestApiView(GenericAPIView):
    serializer_class = FriendshipRequestSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request: Request) -> Response:
        """List all friendship requests sent to current user"""

        friendship_requests = list_friendship_requests(user=request.data.user_id)
        serializer = self.serializer_class(friendship_requests, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        """Send a friendship request to user"""

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            from_user = serializer.validated_data("from_user")
            to_user = serializer.validated_data("to_user")
            try:
                friendship_request = send_friendship_request(from_user=from_user, to_user=to_user)
                serializer = self.serializer_class(friendship_request)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except BadRequest as e:
                return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request_id: int) -> Response:
        """Delete or reject friendship request"""

        delete_friendship_request(request_id=request_id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request: Request, request_id: int) -> Response:
        """Accept friendship request and add to friends list"""

        try:
            accept_friendship_request(user=request.user, request_id=request_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except BadRequest as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
