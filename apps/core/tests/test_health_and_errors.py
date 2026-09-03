from django.test import TestCase, override_settings
from django.urls import reverse


class HealthCheckAndErrorPageTests(TestCase):
    def test_health_check_returns_200_json_healthy(self):
        response = self.client.get(reverse("health_check"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "healthy"})
        self.assertEqual(response.headers.get("X-Robots-Tag"), "noindex, nofollow")

    def test_health_check_excluded_from_sitemap(self):
        response = self.client.get(reverse("sitemap"))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertNotIn("/health/", content)

    @override_settings(DEBUG=False)
    def test_custom_404_page_renders_cyberpunk_theme_and_no_stacktrace(self):
        response = self.client.get("/ruta-inexistente-para-prueba-404/")
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "SEÑAL NO ENCONTRADA", status_code=404)
        self.assertContains(response, 'meta name="robots" content="noindex, nofollow"', status_code=404)
        self.assertContains(response, "Volver al inicio", status_code=404)

    @override_settings(DEBUG=False)
    def test_custom_500_template_is_renderable_without_leaking_secrets(self):
        from django.template.loader import render_to_string

        rendered = render_to_string("500.html")
        self.assertIn("FALLO DEL SISTEMA", rendered)
        self.assertIn('meta name="robots" content="noindex, nofollow"', rendered)
        self.assertIn("Volver al inicio", rendered)
        self.assertNotIn("Traceback", rendered)
        self.assertNotIn("SECRET_KEY", rendered)
