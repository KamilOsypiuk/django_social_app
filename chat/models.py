from django.db import models
from users.models import User
# Create your models here.


class Chat(models.Model):
    participants = models.ManyToManyField(User, related_name='chats')

    class Meta:
        db_table = 'chat'


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    message = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'message'
