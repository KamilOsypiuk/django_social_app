from rest_framework import serializers

from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'timestamp', 'chat_id', 'message']

    def to_representation(self, instance):
        return instance.message
