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

    def test_home_links_only_to_available_internal_routes(self):
        response = self.client.get(reverse("core:home"))

        self.assertContains(response, 'href="/guias/')
        self.assertContains(response, 'href="/estrategias/')
        self.assertContains(response, f'href="{reverse("cards:catalog")}">Explorar Choomdex</a>')
        self.assertNotContains(
            response,
            'Choomdex Hispano</h3><p>Base de datos táctica de cartas en español.</p><span class="badge badge--green">En desarrollo</span>',
        )
        self.assertContains(response, 'Deck Builder</h3><p>Construcción y análisis de mazos.</p><span class="badge badge--green">En desarrollo</span>')
        self.assertContains(response, "Comunidad · Próximamente")

    def test_footer_links_to_editorial_modules_without_future_labels(self):
        response = self.client.get(reverse("core:home"))

        self.assertContains(response, f'href="{reverse("content:guide_list")}">Guías</a>')
        self.assertContains(response, f'href="{reverse("content:strategy_list")}">Estrategias</a>')
        self.assertNotContains(response, "Guías · Próximamente")
        self.assertNotContains(response, "Estrategias · Próximamente")
        self.assertContains(response, "Comunidad · Próximamente")
