from django.test import TestCase
from django.urls import reverse


class HomeViewTests(TestCase):
    def test_home_returns_successfully(self):
        response = self.client.get(reverse("core:home"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/home.html")

    def test_home_exposes_the_phase_two_identity_and_future_tools(self):
        response = self.client.get(reverse("core:home"))

        self.assertContains(response, "JORGE")
        self.assertContains(response, "CYBERPUNKTCG")
        self.assertContains(response, "Tu Cyberdeck táctico para hackear el meta y convertirte en Leyenda.")
        self.assertContains(response, "Choomdex Hispano")
        self.assertContains(response, "Combat Terminal")

    def test_home_only_links_to_available_internal_routes(self):
        response = self.client.get(reverse("core:home"))

        self.assertNotContains(response, 'href="/guias/')
        self.assertNotContains(response, 'href="/estrategias/')
        self.assertNotContains(response, 'href="/choomdex/')
