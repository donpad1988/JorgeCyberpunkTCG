from django.test import TestCase
from django.urls import reverse


class PrivacyAndTermsViewTests(TestCase):
    def test_privacy_policy_view_returns_200_and_expected_content(self):
        response = self.client.get(reverse("core:privacy"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/privacy.html")
        self.assertContains(response, "POLÍTICA DE PRIVACIDAD")
        self.assertContains(response, "jorgecyberpunktcg@gmail.com")
        self.assertContains(response, "JorgeCyberpunkTCG")
        self.assertContains(response, "youtube-nocookie.com")
        self.assertContains(response, '<link rel="canonical" href="http://testserver/privacidad/">')

    def test_terms_of_service_view_returns_200_and_expected_content(self):
        response = self.client.get(reverse("core:terms"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/terms.html")
        self.assertContains(response, "TÉRMINOS DE USO")
        self.assertContains(response, "jorgecyberpunktcg@gmail.com")
        self.assertContains(response, "JorgeCyberpunkTCG es un proyecto independiente de comunidad y contenido táctico. No está afiliado oficialmente con CD PROJEKT RED ni WeirdCo.")
        self.assertContains(response, '<link rel="canonical" href="http://testserver/terminos/">')

    def test_footer_contains_privacy_and_terms_links_and_independent_disclaimer(self):
        response = self.client.get(reverse("core:home"))

        self.assertContains(response, f'href="{reverse("core:privacy")}">Privacidad</a>')
        self.assertContains(response, f'href="{reverse("core:terms")}">Términos</a>')
        self.assertContains(response, "JorgeCyberpunkTCG es un proyecto independiente de comunidad y contenido táctico. No está afiliado oficialmente con CD PROJEKT RED ni WeirdCo.")

    def test_registration_page_contains_legal_notice_links(self):
        response = self.client.get(reverse("accounts:register"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'href="{reverse("core:privacy")}"')
        self.assertContains(response, f'href="{reverse("core:terms")}"')
        self.assertContains(response, "Antes de crear tu cuenta, consulta cómo tratamos tus datos en nuestra")
        self.assertContains(response, "Al crear la cuenta, declaras conocer y aceptar los")
