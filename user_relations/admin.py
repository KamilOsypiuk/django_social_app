from django.contrib import admin

from .models import FriendshipRelation, FriendshipRequest

# Register your models here.

admin.site.register(FriendshipRequest)
admin.site.register(FriendshipRelation)
