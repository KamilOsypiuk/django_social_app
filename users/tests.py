from django.test import TestCase

from .managers import UserManager
from .models import User
# Create your tests here.


class UserManagerTestCase(TestCase):
    def test_create_user_raises_value_error_when_email_is_none(self):
        with self.assertRaises(expected_exception=ValueError):
            UserManager().create_user(email=None, password='')

    def setUp(self) -> None:
        self.user = User.objects.create(email='test@mail.com',
                                        password='testpass',
                                        date_of_birth='1900-01-01',
                                        )

    def test_create_user_correctly_creates_user(self):
        self.assertTrue(User.objects.filter(email=self.user.email).exists())

