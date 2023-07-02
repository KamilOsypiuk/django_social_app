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
        with self.assertRaisesMessage(expected_exception=ServiceException,
                                      expected_message="Can't be friends with yourself"):
            send_friendship_invitation(user=self.user, friend_id=self.user.pk)

    def test_send_friendship_invitation_raises_service_exception_when_invitation_already_exists(self):
        with self.assertRaisesMessage(expected_exception=ServiceException,
                                      expected_message="Invitation already exists"):
            send_friendship_invitation(user=self.user, friend_id=self.user2.pk)
            send_friendship_invitation(user=self.user2, friend_id=self.user.pk)

    def test_are_friends_returns_correct_boolean_value_whether_users_are_friends_already_or_not(self):
        self.assertFalse(are_friends(user1=self.user, user2=self.user2.pk))
        self.user.friends.add(self.user2)
        self.assertTrue(are_friends(user1=self.user, user2=self.user2.pk))

    def test_send_friendship_invitation_sends_invitation_correctly(self):
        send_friendship_invitation(user=self.user, friend_id=self.user2.pk)
        self.assertTrue(User.friend_invitations.through.objects.get(from_user_id=self.user.pk,
                                                                    to_user_id=self.user2.pk))

    def test_delete_friendship_invitation_deletes_invitation_correctly(self):
        queryset = User.friend_invitations.through.objects.filter(Q(from_user_id=self.user) | Q(to_user_id=self.user))

        send_friendship_invitation(user=self.user, friend_id=self.user2.pk)
        invitation = User.friend_invitations.through.objects.get(from_user_id=self.user.pk, to_user_id=self.user2.pk)
        delete_friendship_invitation(user=self.user, invitation_id=invitation.id, queryset=queryset)
        invitation_exists = User.friend_invitations.through.objects.filter(from_user_id=self.user.pk,
                                                                           to_user_id=self.user2.pk).exists()
        self.assertFalse(invitation_exists)

    def test_accept_friendship_invitation_removes_invitation_and_adds_user_to_friends(self):
        queryset = User.friend_invitations.through.objects.filter(Q(from_user_id=self.user) | Q(to_user_id=self.user))

        send_friendship_invitation(user=self.user, friend_id=self.user2.pk)
        invitation = User.friend_invitations.through.objects.get(from_user_id=self.user.pk, to_user_id=self.user2.pk)
        accept_friendship_invitation(user=self.user2, invitation_id=invitation.id, queryset=queryset)
        invitation_exists = User.friend_invitations.through.objects.filter(from_user_id=self.user.pk,
                                                                           to_user_id=self.user2.pk).exists()
        self.assertFalse(invitation_exists)

        friend_list = User.friends.through.objects.filter(Q(from_user_id=self.user.pk, to_user_id=self.user2.pk) |
                                                          Q(from_user_id=self.user2.pk, to_user_id=self.user.pk))
        self.assertTrue(friend_list)

    def test_accept_friendship_invitation_raises_service_exception_when_sender_tries_to_accept(self):
        queryset = User.friend_invitations.through.objects.filter(Q(from_user_id=self.user) | Q(to_user_id=self.user))

        with self.assertRaisesMessage(expected_exception=ServiceException,
                                      expected_message="You can't accept this invitation as sender"):
            send_friendship_invitation(user=self.user, friend_id=self.user2.pk)
            invitation = User.friend_invitations.through.objects.get(from_user_id=self.user.pk,
                                                                     to_user_id=self.user2.pk)
            accept_friendship_invitation(user=self.user, invitation_id=invitation.id, queryset=queryset)


class FriendshipRelationServicesTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            email="test@mail.com",
            password="testpass",
        )
        self.user2 = User.objects.create(
            email="test2@mail.com",
            password="testpass",
        )

    def test_delete_friend_deletes_correctly(self):
        queryset = User.friends.through.objects.filter(from_user_id=self.user)

        self.user.friends.add(self.user2.pk)

        relation = User.friends.through.objects.get(from_user_id=self.user.pk, to_user_id=self.user2.pk)
        delete_friend(user=self.user, relation_id=relation.id, queryset=queryset)

        relation_exists = User.friends.through.objects.filter(from_user_id=self.user.pk,
                                                              to_user_id=self.user2.pk).exists()
        self.assertFalse(relation_exists)


class BlockServicesTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            email="test@mail.com",
            password="testpass",
        )
        self.user2 = User.objects.create(
            email="test2@mail.com",
            password="testpass",
        )

    def test_block_user_raises_service_exception_if_relation_is_blocked_already(self):
        with self.assertRaisesMessage(expected_exception=ServiceException,
                                      expected_message='This relation is blocked already'):
            self.user.blocks.add(self.user2.pk)

            block_user(user=self.user, user_id=self.user2.pk)

    def test_block_user_raises_service_exception_if_user_tries_to_block_himself(self):
        with self.assertRaisesMessage(expected_exception=ServiceException,
                                      expected_message="You can't block yourself"):
            block_user(user=self.user, user_id=self.user.pk)

    def test_block_user_creates_block_relation_correctly(self):
        block_user(user=self.user, user_id=self.user2.pk)
        block_relation = User.blocks.through.objects.filter(from_user_id=self.user.pk, to_user_id=self.user2.pk).exists()
        self.assertTrue(block_relation)

    def test_unblock_user_raises_service_exception_if_blocked_user_tries_to_unblock_relation(self):
        queryset = User.blocks.through.objects.filter(Q(from_user_id=self.user.pk) | Q(to_user_id=self.user.pk))

        with self.assertRaisesMessage(expected_exception=ServiceException,
                                      expected_message="You can't unblock this user because you have been blocked"):
            block_user(user=self.user, user_id=self.user2.pk)
            block = User.blocks.through.objects.get(from_user_id=self.user, to_user_id=self.user2)
            unblock_user(user=self.user2, block_id=block.id, queryset=queryset)

    def test_unblock_user_removes_block_correctly(self):
        queryset = User.blocks.through.objects.filter(Q(from_user_id=self.user.pk) | Q(to_user_id=self.user.pk))

        block_user(user=self.user, user_id=self.user2.pk)
        block = User.blocks.through.objects.get(from_user_id=self.user, to_user_id=self.user2)
        unblock_user(user=self.user, block_id=block.id, queryset=queryset)
        unblocked_relation = User.blocks.through.objects.filter(from_user_id=self.user.pk,
                                                                to_user_id=self.user2.pk).exists()
        self.assertFalse(unblocked_relation)
