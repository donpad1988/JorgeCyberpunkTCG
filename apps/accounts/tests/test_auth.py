from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from django.urls import reverse


class AuthenticationFlowTests(TestCase):
    password = "Secure-pass-2026!"

    def create_user(self, username="netrunner", email="netrunner@example.com"):
        return get_user_model().objects.create_user(username=username, email=email, password=self.password)

    def test_registration_creates_and_authenticates_user(self):
        self.assertEqual(self.client.get(reverse("accounts:register")).status_code, 200)
        response = self.client.post(reverse("accounts:register"), {"username": "newrunner", "email": "newrunner@example.com", "password1": self.password, "password2": self.password})

        user = get_user_model().objects.get(username="newrunner")
        self.assertRedirects(response, reverse("accounts:profile"))
        self.assertTrue(user.check_password(self.password))
        self.assertEqual(self.client.session.get("_auth_user_id"), str(user.pk))

    def test_registration_rejects_duplicate_username_and_mismatched_passwords(self):
        self.create_user()
        response = self.client.post(reverse("accounts:register"), {"username": "netrunner", "email": "another@example.com", "password1": self.password, "password2": "different-pass-2026!"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ya existe un usuario con este nombre.")
        self.assertContains(response, "Los dos campos de contraseña no coinciden.")

    def test_login_and_post_only_logout(self):
        user = self.create_user()
        self.assertEqual(self.client.get(reverse("accounts:login")).status_code, 200)
        response = self.client.post(reverse("accounts:login"), {"username": user.username, "password": self.password})
        self.assertRedirects(response, reverse("accounts:profile"))
        self.assertEqual(self.client.get(reverse("accounts:logout")).status_code, 405)
        response = self.client.post(reverse("accounts:logout"))
        self.assertRedirects(response, reverse("core:home"))
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_invalid_login_does_not_authenticate(self):
        self.create_user()
        response = self.client.post(reverse("accounts:login"), {"username": "netrunner", "password": "wrong-password"})

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_password_reset_sends_native_token_link(self):
        self.create_user()
        self.assertEqual(self.client.get(reverse("accounts:password_reset")).status_code, 200)
        response = self.client.post(reverse("accounts:password_reset"), {"email": "netrunner@example.com"})

        self.assertRedirects(response, reverse("accounts:password_reset_done"))
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("password-reset", mail.outbox[0].body)
        reset_path = urlparse(re.search(r"http://testserver(?P<path>/cuenta/password-reset/[^\s]+)", mail.outbox[0].body).group("path")).path
        self.assertEqual(self.client.get(reset_path, follow=True).status_code, 200)
import re
from urllib.parse import urlparse
