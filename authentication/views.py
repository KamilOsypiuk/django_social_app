from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from .services import register_user
from .serializers import UserRegisterSerializer


# Create your views here.


class RegisterUserApiView(GenericAPIView):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()

    def post(self, request: Request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        register_user(request, **serializer.validated_data)
        return Response("Account created successfully", status=status.HTTP_201_CREATED)




