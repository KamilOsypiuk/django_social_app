from django.db.models import Q, QuerySet
from django.shortcuts import get_object_or_404

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

    else:
        User.friend_invitations.through.objects.create(from_user_id=user.pk, to_user_id=friend_id)
        return {'message': 'Friend invitation sent'}


def list_friendship_invitations(user: User, queryset: QuerySet) -> list:
    if friendship_invitation_list := queryset.filter(Q(to_user_id=user.pk) | Q(from_user_id=user.pk)):
        return friendship_invitation_list
    else:
        raise ServiceException('There is no invites associated with this user')


def delete_friendship_invitation(user: User, friend_id: int, queryset: QuerySet) -> dict:
    invitation = queryset.filter(Q(from_user_id=user.pk, to_user_id=friend_id) |
                                 Q(from_user_id=friend_id, to_user_id=user.pk)).first()
    if user.pk in [invitation.from_user_id, invitation.to_user_id]:
        user.friend_invitations.remove(friend_id)
        return {'message': 'Friend invitation rejected'}
    else:
        raise ServiceException("You can't delete or reject this invitation")


def accept_friendship_invitation(user: User, friend_id: int, queryset: QuerySet) -> dict:
    invitation = get_object_or_404(queryset, from_user_id=friend_id, to_user_id=user.pk)

    if invitation.to_user_id != user.pk:
        raise ServiceException("You can't accept this invitation")
    else:
        user.friends.add(friend_id)
        user.friend_invitations.remove(friend_id)
        return {'message': 'Friend invitation accepted'}
