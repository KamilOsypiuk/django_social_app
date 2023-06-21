from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

from .managers import UserManager

# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, blank=False, max_length=225)
    date_of_birth = models.DateField(blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    friend_invitations = models.ManyToManyField('self', default=None)
    friends = models.ManyToManyField('self', default=None)
    blocks = models.ManyToManyField('self', default=None)
    is_staff = models.BooleanField(
        default=False,
        help_text=("Designates whether the user can log into " "this admin site."),
    )
    is_active = models.BooleanField(
        default=True,
        help_text=(
            "Designates whether this user should be "
            "treated as active. Unselect this instead "
            "of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = "auth_user"
