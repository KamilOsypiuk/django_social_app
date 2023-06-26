from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from users.models import User
from relations.services import send_friendship_invitation


# Create your tests here.


class FriendshipInvitationApiViewTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            email='test@mail.com',
            password='testpass')
        self.user2 = User.objects.create(
            email='test2@mail.com',
            password='testpass'
        )

    def test_authenticated_user_can_access_send_invitation_protected_endpoint(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(reverse('send-friend-invitation', kwargs={'friend_id': self.user2.pk}))
        self.assertEqual(response.status_code, 201)

    def test_authenticated_user_can_access_get_invitations_protected_endpoint(self):
        self.client.force_authenticate(user=self.user)

        send_friendship_invitation(user=self.user, friend_id=self.user2.pk)

        response = self.client.get(reverse('friend-invitation'))
        self.assertEqual(response.status_code, 200)

    def test_authenticated_user_can_access_delete_invitation_protected_endpoint(self):
        self.client.force_authenticate(user=self.user)

        send_friendship_invitation(user=self.user, friend_id=self.user2.pk)

        response = self.client.delete(reverse('delete-friend-invitation', kwargs={'friend_id': self.user2.pk}))
        self.assertEqual(response.status_code, 200)

    def test_authenticated_user_can_access_accept_invitation_protected_endpoint(self):
        self.client.force_authenticate(user=self.user2)

        send_friendship_invitation(user=self.user, friend_id=self.user2.pk)

        response = self.client.put(reverse('accept-friend-invitation', kwargs={'friend_id': self.user.pk}))
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_users_can_not_access_protected_endpoints(self):
        response = self.client.get(reverse('friend-invitation'))
        self.assertEqual(response.status_code, 401)

        response = self.client.post(reverse('send-friend-invitation', kwargs={'friend_id': self.user2.pk}))
        self.assertEqual(response.status_code, 401)

        response = self.client.delete(reverse('delete-friend-invitation', kwargs={'friend_id': self.user2.pk}))
        self.assertEqual(response.status_code, 401)

        response = self.client.put(reverse('accept-friend-invitation', kwargs={'friend_id': self.user2.pk}))
        self.assertEqual(response.status_code, 401)



