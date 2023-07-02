from django.db.models import Q, QuerySet
from django.shortcuts import get_object_or_404

from rest_framework.exceptions import NotFound

from users.models import User
from .exeptions import ServiceException


def are_friends(user1: User, user2: int) -> bool:
    if User.objects.filter(Q(id=user2, friends=user1.pk) | (Q(id=user1.pk, friends=user2))):
        return True

    else:
        return False


def send_friendship_invitation(user: User, friend_id: int) -> dict:
    if User.objects.filter(Q(id=user.pk, friend_invitations=friend_id) | (Q(id=friend_id, friend_invitations=user.pk))):
        raise ServiceException("Invitation already exists")

    if user.pk == friend_id:
        raise ServiceException("Can't be friends with yourself")

    if are_friends(user1=user, user2=friend_id):
        raise ServiceException("You are friends already")

    if User.objects.get(id=friend_id) is None:
        raise NotFound("User with that id doesn't exist")

    else:
        User.friend_invitations.through.objects.create(from_user_id=user.pk, to_user_id=friend_id)
        return {'message': 'Friend invitation sent'}


def delete_friendship_invitation(user: User, invitation_id: int, queryset: QuerySet) -> dict:
    invitation = get_object_or_404(queryset, id=invitation_id)
    if user.pk in [invitation.from_user_id, invitation.to_user_id]:
        invitation.delete()
        return {'message': 'Friend invitation rejected'}


def accept_friendship_invitation(user: User, invitation_id: int, queryset: QuerySet) -> dict:
    invitation = get_object_or_404(queryset, id=invitation_id)

    if invitation.to_user_id != user.pk:
        raise ServiceException("You can't accept this invitation as sender")
    else:
        user.friends.add(invitation.from_user_id)
        user.friend_invitations.remove(invitation.from_user_id)
        return {'message': 'Friend invitation accepted'}


def delete_friend(user: User, relation_id: int, queryset: QuerySet) -> dict:
    friend = get_object_or_404(queryset, id=relation_id)

    if friend:
        user.friends.remove(friend.to_user_id)
        return {'message': 'Friend removed successfully'}


def are_blocked_already(user1: User, user2: int) -> bool:
    if User.objects.filter(Q(id=user2, blocks=user1.pk) | (Q(id=user1.pk, blocks=user2))):
        return True

    else:
        return False


def block_user(user: User, user_id: int) -> dict:
    if are_blocked_already(user1=user, user2=user_id):
        raise ServiceException('This relation is blocked already')

    if user.pk == user_id:
        raise ServiceException("You can't block yourself")

    else:
        User.blocks.through.objects.create(from_user_id=user.pk, to_user_id=user_id)
        return {'message': 'User blocked successfully'}


def unblock_user(user: User, block_id: int, queryset: QuerySet) -> dict:
    block = get_object_or_404(queryset, id=block_id)

    if block.from_user_id != user.pk:
        raise ServiceException("You can't unblock this user because you have been blocked")
    else:
        user.blocks.remove(block.to_user_id)
        return {'message': 'Unblocked user successfully'}
