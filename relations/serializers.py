from rest_framework import serializers

from users.models import User


class UserFriendInvitationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User.friend_invitations.through
        fields = ['id', 'from_user_id', 'to_user_id']


class UserFriendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User.friends.through
        fields = ['id', 'from_user_id', 'to_user_id']


class UserBlocksSerializer(serializers.ModelSerializer):
    class Meta:
        model = User.blocks.through
        fields = ['id', 'from_user_id', 'to_user_id']
