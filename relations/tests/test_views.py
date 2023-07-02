from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from users.models import User


# Create your tests here.


class FriendshipInvitationApiViewTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            email='test@mail.com',
            password='testpass')
        self.user2 = User.objects.create(
            email='test2@mail.com',
            password='testpass')
        self.user3 = User.objects.create(
            email='test3@mail.com',
            password='testpass'
        )

    def test_authenticated_user_can_access_send_invitation_protected_endpoint(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(reverse('friend-invitation-send', kwargs={'friend_id': self.user2.pk}))
        self.assertEqual(response.status_code, 201)

    def test_friendship_invitation_send_view_returns_400_status_code_if_invitation_exists_already(self):
        self.client.force_authenticate(user=self.user)

        self.client.post(reverse('friend-invitation-send', kwargs={'friend_id': self.user2.pk}))
        response = self.client.post(reverse('friend-invitation-send', kwargs={'friend_id': self.user2.pk}))

        self.assertEqual(response.status_code, 400)

    def test_friendship_invitation_send_view_returns_400_status_code_if_user_sends_invite_to_themself(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(reverse('friend-invitation-send', kwargs={'friend_id': self.user.pk}))

        self.assertEqual(response.status_code, 400)

    def test_friendship_invitation_send_view_returns_400_status_code_if_user_sends_invite_to_their_friend(self):
        self.client.force_authenticate(user=self.user)

        self.user.friends.add(self.user2.pk)
        response = self.client.post(reverse('friend-invitation-send', kwargs={'friend_id': self.user2.pk}))

        self.assertEqual(response.status_code, 400)

    def test_authenticated_user_can_access_friend_invitation_list_protected_endpoint(self):
        self.client.force_authenticate(user=self.user)

        self.user.friend_invitations.add(self.user2.pk)
        response = self.client.get(reverse('friend-invitation-list'))

        self.assertEqual(response.status_code, 200)

    def test_authenticated_user_can_access_friend_invitation_delete_protected_endpoint(self):
        self.client.force_authenticate(user=self.user)

        self.user.friend_invitations.add(self.user2.pk)
        invitation = User.friend_invitations.through.objects.get(from_user_id=self.user.pk, to_user_id=self.user2.pk)
        response = self.client.delete(reverse('friend-invitation-delete', kwargs={'invitation_id': invitation.id}))

        self.assertEqual(response.status_code, 200)

    def test_friend_invitation_delete_view_returns_404_status_code_if_not_included_user_in_invitation_tries_delete(self):
        self.client.force_authenticate(user=self.user3)

        self.user.friend_invitations.add(self.user2.pk)
        invitation = User.friend_invitations.through.objects.get(from_user_id=self.user.pk, to_user_id=self.user2.pk)
        response = self.client.delete(reverse('friend-invitation-delete', kwargs={'invitation_id': invitation.id}))

        self.assertEqual(response.status_code, 404)

    def test_authenticated_user_can_access_friend_invitation_accept_protected_endpoint(self):
        self.client.force_authenticate(user=self.user2)

        self.user.friend_invitations.add(self.user2.pk)
        invitation = User.friend_invitations.through.objects.get(from_user_id=self.user.pk, to_user_id=self.user2.pk)
        response = self.client.put(reverse('friend-invitation-accept', kwargs={'invitation_id': invitation.id}))

        self.assertEqual(response.status_code, 200)

    def test_friend_invitation_accept_view_returns_404_status_code_if_not_included_user_in_invitation_tries_accept(self):
        self.client.force_authenticate(user=self.user3)

        self.user.friend_invitations.add(self.user2.pk)
        invitation = User.friend_invitations.through.objects.get(from_user_id=self.user.pk, to_user_id=self.user2.pk)
        response = self.client.put(reverse('friend-invitation-accept', kwargs={'invitation_id': invitation.id}))

        self.assertEqual(response.status_code, 404)

    def test_friend_invitation_accept_view_returns_400_status_code_if_sender_tries_to_accept_invitation(self):
        self.client.force_authenticate(user=self.user)

        self.client.post(reverse('friend-invitation-send', kwargs={'friend_id': self.user2.pk}))
        invitation = User.friend_invitations.through.objects.get(from_user_id=self.user.pk, to_user_id=self.user2.pk)
        response = self.client.put(reverse('friend-invitation-accept', kwargs={'invitation_id': invitation.id}))

        self.assertEqual(response.status_code, 400)

    def test_unauthenticated_users_can_not_access_friend_invitation_list_protected_endpoint(self):
        response = self.client.get(reverse('friend-invitation-list'))
        self.assertEqual(response.status_code, 401)

    def test_unauthenticated_users_can_not_access_friend_invitation_send_protected_endpoint(self):
        response = self.client.post(reverse('friend-invitation-send', kwargs={'friend_id': self.user2.pk}))
        self.assertEqual(response.status_code, 401)

    def test_unauthenticated_users_can_not_access_friend_invitation_delete_protected_endpoint(self):
        self.user.friend_invitations.add(self.user2.pk)
        invitation = User.friend_invitations.through.objects.get(from_user_id=self.user.pk, to_user_id=self.user2.pk)
        response = self.client.delete(reverse('friend-invitation-delete', kwargs={'invitation_id': invitation.id}))
        self.assertEqual(response.status_code, 401)

    def test_unauthenticated_users_can_not_access_friend_invitation_accept_protected_endpoint(self):
        self.user.friend_invitations.add(self.user2.pk)
        invitation = User.friend_invitations.through.objects.get(from_user_id=self.user.pk, to_user_id=self.user2.pk)
        response = self.client.put(reverse('friend-invitation-accept', kwargs={'invitation_id': invitation.id}))
        self.assertEqual(response.status_code, 401)


class FriendshipRelationApiViewTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            email='test@mail.com',
            password='testpass')
        self.user2 = User.objects.create(
            email='test2@mail.com',
            password='testpass'
        )
        self.user3 = User.objects.create(
            email='test3@mail.com',
            password='testpass'
        )

    def test_authenticated_user_can_access_friend_list_protected_endpoint(self):
        self.client.force_authenticate(user=self.user)

        self.user.friends.add(self.user2.pk)

        response = self.client.get(reverse('friend-list'))
        self.assertEqual(response.status_code, 200)

    def test_authenticated_user_can_access_friend_delete_protected_endpoint(self):
        self.client.force_authenticate(user=self.user)

        self.user.friends.add(self.user2.pk)

        relation = User.friends.through.objects.get(from_user_id=self.user.pk, to_user_id=self.user2.pk)
        response = self.client.delete(reverse('friend-delete', kwargs={'relation_id': relation.id}))
        self.assertEqual(response.status_code, 200)

    def test_friend_delete_view_returns_404_status_code_if_not_included_user_in_relation_tries_delete(self):
        self.client.force_authenticate(user=self.user3)

        self.user.friends.add(self.user2.pk)

        relation = User.friends.through.objects.get(from_user_id=self.user.pk, to_user_id=self.user2.pk)
        response = self.client.delete(reverse('friend-delete', kwargs={'relation_id': relation.id}))

        self.assertEqual(response.status_code, 404)

    def test_unauthenticated_users_can_not_access_friend_list_protected_endpoint(self):
        response = self.client.get(reverse('friend-list'))
        self.assertEqual(response.status_code, 401)

    def test_unauthenticated_users_can_not_access_friend_delete_protected_endpoint(self):
        self.user.friends.add(self.user2.pk)
        relation = User.friends.through.objects.get(from_user_id=self.user.pk, to_user_id=self.user2.pk)
        response = self.client.delete(reverse('friend-delete', kwargs={'relation_id': relation.id}))
        self.assertEqual(response.status_code, 401)


class BlockApiViewTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            email='test@mail.com',
            password='testpass')
        self.user2 = User.objects.create(
            email='test2@mail.com',
            password='testpass'
        )
        self.user3 = User.objects.create(
            email='test3@mail.com',
            password='testpass'
        )

    def test_authenticated_user_can_access_blocked_users_list_protected_endpoint(self):
        self.client.force_authenticate(user=self.user)

        self.user.blocks.add(self.user2.pk)

        response = self.client.get(reverse('blocked-users-list'))
        self.assertEqual(response.status_code, 200)

    def test_authenticated_user_can_access_block_user_protected_endpoint(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(reverse('block-user', kwargs={'user_id': self.user2.pk}))
        self.assertEqual(response.status_code, 201)

    def test_block_user_view_returns_400_status_code_if_relation_between_users_is_blocked_already(self):
        self.client.force_authenticate(user=self.user)

        self.user.blocks.add(self.user2.pk)
        response = self.client.post(reverse('block-user', kwargs={'user_id': self.user2.pk}))

        self.assertEqual(response.status_code, 400)

    def test_block_user_view_returns_400_status_code_if_users_tries_block_themself(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(reverse('block-user', kwargs={'user_id': self.user.pk}))

        self.assertEqual(response.status_code, 400)

    def test_authenticated_user_can_access_unblock_user_protected_endpoint(self):
        self.client.force_authenticate(user=self.user)

        self.user.blocks.add(self.user2.pk)

        block = User.blocks.through.objects.get(from_user_id=self.user.pk, to_user_id=self.user2.pk)
        response = self.client.delete(reverse('unblock-user', kwargs={'block_id': block.id}))
        self.assertEqual(response.status_code, 200)

    def test_unblock_user_view_returns_400_status_code_if_blocked_user_tries_to_unblock(self):
        self.client.force_authenticate(user=self.user)
        self.client.post(reverse('block-user', kwargs={'user_id': self.user2.pk}))

        self.client.force_authenticate(user=self.user2)
        block = User.blocks.through.objects.get(from_user_id=self.user.pk, to_user_id=self.user2.pk)
        response = self.client.delete(reverse('unblock-user', kwargs={'block_id': block.id}))

        self.assertEqual(response.status_code, 400)

    def test_unblock_user_view_returns_404_status_code_if_not_included_user_in_block_relation_tries_unblock(self):
        self.client.force_authenticate(user=self.user3)

        self.user.blocks.add(self.user2.pk)
        block = User.blocks.through.objects.get(from_user_id=self.user.pk, to_user_id=self.user2.pk)
        response = self.client.delete(reverse('unblock-user', kwargs={'block_id': block.id}))

        self.assertEqual(response.status_code, 404)

    def test_unauthenticated_users_can_not_access_blocked_users_list_protected_endpoint(self):
        response = self.client.get(reverse('blocked-users-list'))
        self.assertEqual(response.status_code, 401)

    def test_unauthenticated_users_can_not_access_block_user_protected_endpoint(self):
        response = self.client.post(reverse('block-user', kwargs={'user_id': self.user2.pk}))
        self.assertEqual(response.status_code, 401)

    def test_unauthenticated_users_can_not_access_unblock_user_protected_endpoint(self):
        self.user.blocks.add(self.user2.pk)
        block = User.blocks.through.objects.get(from_user_id=self.user.pk, to_user_id=self.user2.pk)
        response = self.client.delete(reverse('unblock-user', kwargs={'block_id': block.id}))
        self.assertEqual(response.status_code, 401)
