from django.core.exceptions import BadRequest

from users.models import User

from .models import FriendshipRelation, FriendshipRequest


def are_friends(user1: User, user2: User) -> bool:
    if FriendshipRelation.objects.filter(user=user2, friends=user1):
        return True

    if FriendshipRelation.objects.filter(user=user1, friends=user2):
        return True

    else:
        return False


def send_friendship_request(from_user: User, to_user: User) -> FriendshipRequest:
    if FriendshipRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
        raise BadRequest("Request already exists")

    if FriendshipRequest.objects.filter(from_user=to_user, to_user=from_user).exists():
        raise BadRequest("Request already exists")

    if from_user == to_user:
        raise BadRequest("Can't be friends with yourself")

    if are_friends(user1=from_user, user2=to_user):
        raise BadRequest("You are friends already")

    else:
        friendship_request = FriendshipRequest.objects.create(
            from_user=from_user, to_user=to_user
        )
        return friendship_request


def list_friendship_requests(user: User) -> list:
    friendship_request_list = FriendshipRequest.objects.all().filter(to_user=user)
    return friendship_request_list


def delete_friendship_request(request_id: int) -> None:
    friendship_request = FriendshipRequest.objects.get(id=request_id)
    friendship_request.delete()


def accept_friendship_request(user: User, request_id: int) -> None:
    friendship_request = FriendshipRequest.objects.get(id=request_id)

    if friendship_request.to_user != user:
        raise BadRequest("You can't accept an invitation you sent yourself")

    else:
        user_relation = FriendshipRelation.objects.get_or_create(user=user)
        user_relation.friends.add(friendship_request.from_user)

        from_user_relation = FriendshipRelation.objects.get_or_create(
            user=friendship_request.from_user
        )
        from_user_relation.friends.add(user)

        friendship_request.delete()
