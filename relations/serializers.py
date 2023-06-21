from rest_framework import serializers

from users.models import User


class UserFriendInvitationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User.friend_invitations.through
        fields = ['from_user_id', 'to_user_id']
