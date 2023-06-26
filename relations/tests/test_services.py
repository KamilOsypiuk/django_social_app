from django.db.models import Q
from django.test import TestCase

from relations.exeptions import ServiceException
from relations.services import *
from users.models import User


class FriendshipInvitationServicesTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            email="test@mail.com",
            password="testpass",
        )
        self.user2 = User.objects.create(
            email="test2@mail.com",
            password="testpass",
        )

    def test_send_friendship_invitation_raises_service_exception_when_user_and_friend_has_the_same_id(self):

        with self.assertRaises(expected_exception=ServiceException):
            send_friendship_invitation(user=self.user, friend_id=self.user.pk)

    def test_send_friendship_invitation_raises_service_exception_when_invitation_already_exists(self):
        with self.assertRaises(expected_exception=ServiceException):
            send_friendship_invitation(user=self.user, friend_id=self.user2.pk)
            send_friendship_invitation(user=self.user2, friend_id=self.user.pk)

    def test_are_friends_returns_correct_boolean_value_whether_users_are_friends_already_or_not(self):
        self.assertFalse(are_friends(user1=self.user, user2=self.user2.pk))
        user = self.user
        user.friends.add(self.user2)
        self.assertTrue(are_friends(user1=self.user, user2=self.user2.pk))

    def test_send_friendship_invitation_sends_invitation_correctly(self):
        send_friendship_invitation(user=self.user, friend_id=self.user2.pk)
        self.assertTrue(User.friend_invitations.through.objects.get(from_user_id=self.user.pk,
                                                                    to_user_id=self.user2.pk))

    def test_list_friendship_invitations_returns_list_correctly(self):
        queryset = User.friend_invitations.through.objects.filter(Q(from_user_id=self.user) | Q(to_user_id=self.user))

        with self.assertRaises(expected_exception=ServiceException):
            list_friendship_invitations(user=self.user, queryset=queryset)

        send_friendship_invitation(user=self.user, friend_id=self.user2.pk)
        result = list_friendship_invitations(user=self.user, queryset=queryset)
        self.assertEqual(set(result), set(queryset))

    def test_delete_friendship_invitation_deletes_invitation_correctly(self):
        queryset = User.friend_invitations.through.objects.filter(Q(from_user_id=self.user) | Q(to_user_id=self.user))

        send_friendship_invitation(user=self.user, friend_id=self.user2.pk)
        delete_friendship_invitation(user=self.user, friend_id=self.user2.pk, queryset=queryset)
        self.assertFalse(queryset.exists())

    def test_accept_friendship_invitation_removes_invitation_and_adds_user_to_friends(self):
        queryset = User.friend_invitations.through.objects.filter(Q(from_user_id=self.user) | Q(to_user_id=self.user))

        send_friendship_invitation(user=self.user, friend_id=self.user2.pk)
        accept_friendship_invitation(user=self.user2, friend_id=self.user.pk, queryset=queryset)
        self.assertFalse(queryset.exists())

        friend_list = User.friends.through.objects.filter(Q(from_user_id=self.user.pk, to_user_id=self.user2.pk) |
                                                          Q(from_user_id=self.user2.pk, to_user_id=self.user.pk))
        self.assertTrue(friend_list.exists())
