from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.exceptions import ValidationError


def register_user(request, **user_data) -> User:
    validate_email(email=user_data.get("email"))
    user = User.objects.create_user(**user_data)
    authenticate(request, username=user_data.get("username"), password=user_data.get("password"))
    login(request, user)
    return user


def validate_email(email):
    if User.objects.filter(email=email).exists():
        raise ValidationError("Email already exist", code=status.HTTP_400_BAD_REQUEST)
    return email
