import importlib
import os
from unittest.mock import patch
from django.test import SimpleTestCase


class ProductionSecuritySettingsTests(SimpleTestCase):
    """
    Regression test suite to ensure production security settings in config.settings.production
    maintain strict security hardening flags without exposing real environment secrets.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Ephemeral, non-sensitive environment variables for isolated module import test
        cls.env_patcher = patch.dict(
            os.environ,
            {
                "DJANGO_SECRET_KEY": "ephemeral-dummy-key-for-local-security-tests-only",
                "DJANGO_ALLOWED_HOSTS": "jorgecyberpunktcg.pythonanywhere.com",
                "DJANGO_CSRF_TRUSTED_ORIGINS": "https://jorgecyberpunktcg.pythonanywhere.com",
            },
        )
        cls.env_patcher.start()
        cls.prod_settings = importlib.import_module("config.settings.production")
        importlib.reload(cls.prod_settings)

    @classmethod
    def tearDownClass(cls):
        cls.env_patcher.stop()
        super().tearDownClass()

    def test_production_debug_is_false(self):
        self.assertIs(self.prod_settings.DEBUG, False)

    def test_production_ssl_redirect_is_true(self):
        self.assertIs(self.prod_settings.SECURE_SSL_REDIRECT, True)

    def test_production_session_cookie_secure_is_true(self):
        self.assertIs(self.prod_settings.SESSION_COOKIE_SECURE, True)

    def test_production_csrf_cookie_secure_is_true(self):
        self.assertIs(self.prod_settings.CSRF_COOKIE_SECURE, True)

    def test_production_content_type_nosniff_is_true(self):
        self.assertIs(self.prod_settings.SECURE_CONTENT_TYPE_NOSNIFF, True)

    def test_production_x_frame_options_is_deny(self):
        self.assertEqual(self.prod_settings.X_FRAME_OPTIONS, "DENY")

    def test_production_hsts_seconds_is_greater_than_zero(self):
        self.assertGreater(self.prod_settings.SECURE_HSTS_SECONDS, 0)
        self.assertEqual(self.prod_settings.SECURE_HSTS_SECONDS, 3600)

    def test_production_hsts_include_subdomains_is_false(self):
        self.assertIs(self.prod_settings.SECURE_HSTS_INCLUDE_SUBDOMAINS, False)

    def test_production_hsts_preload_is_false(self):
        self.assertIs(self.prod_settings.SECURE_HSTS_PRELOAD, False)
