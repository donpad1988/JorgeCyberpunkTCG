from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.test import TestCase, override_settings


class UserModelTests(TestCase):
    def test_custom_user_can_be_created_with_django_password_hashing(self):
        user = get_user_model().objects.create_user(
            username="foundation-test-user", password="test-password-not-a-real-secret"
        )

        self.assertTrue(user.check_password("test-password-not-a-real-secret"))
        self.assertNotEqual(user.password, "test-password-not-a-real-secret")
        self.assertIsInstance(user, AbstractUser)

    def test_auth_user_model_points_to_custom_user(self):
        self.assertEqual(get_user_model()._meta.label, "accounts.User")
