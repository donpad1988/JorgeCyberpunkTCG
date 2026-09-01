from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class ProfileTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="profile-runner", email="profile@example.com", password="Secure-pass-2026!")

    def test_profile_requires_login_and_shows_only_authenticated_identity(self):
        response = self.client.get(reverse("accounts:profile"))
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('accounts:profile')}")
        self.client.force_login(self.user)
        response = self.client.get(reverse("accounts:profile"))
        self.assertContains(response, "@profile-runner")

    def test_profile_edit_updates_only_allowed_fields(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("accounts:profile_edit"), {"first_name": "Jorge", "last_name": "Runner", "email": "jorge@example.com"})

        self.assertRedirects(response, reverse("accounts:profile"))
        self.user.refresh_from_db()
        self.assertEqual((self.user.first_name, self.user.last_name, self.user.email), ("Jorge", "Runner", "jorge@example.com"))

    def test_navigation_and_home_change_with_authentication_state(self):
        response = self.client.get(reverse("core:home"))
        self.assertContains(response, "Jack In")
        self.client.force_login(self.user)
        response = self.client.get(reverse("core:home"))
        self.assertContains(response, "@profile-runner")
        self.assertContains(response, "Jack Out")
