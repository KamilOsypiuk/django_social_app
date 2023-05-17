from abc import ABC

from django.contrib.auth.models import User
from rest_framework import serializers, status
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()

    def validate_password(self, password):
        validate_password(password)
        return password


