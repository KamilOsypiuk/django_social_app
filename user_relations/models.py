from django.db import models

from users.models import User

# Create your models here.


class FriendshipRequest(models.Model):
    """Model to represent friendship requests"""

    from_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="friendship_request_sender"
    )
    to_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="friendship_request_receiver"
    )

    class Meta:
        db_table = "friendship_request"


class FriendshipRelation(models.Model):
    """Model to represent relations between users"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user", default=None, null=True)
    friends = models.ManyToManyField(User, blank=True, related_name="friends")
    blocked = models.BooleanField(default=False)

    class Meta:
        db_table = "friendship_relation"


class Block(models.Model):
    """Model to represent blocked relation between users"""

    blocked_by_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blocker"
    )
    blocked_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blocked"
    )
    friendship_relation = models.ForeignKey(
        FriendshipRelation, on_delete=models.CASCADE, related_name="blocks", default=None, null=True
    )

    class Meta:
        db_table = "block"
