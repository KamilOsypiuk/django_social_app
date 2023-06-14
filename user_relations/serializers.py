from rest_framework import serializers

from .models import FriendshipRelation, FriendshipRequest


class FriendshipRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendshipRequest
        fields = "__all__"


class FriendshipRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendshipRelation
        fields = "__all__"
