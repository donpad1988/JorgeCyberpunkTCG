from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("privacidad/", views.privacy_policy, name="privacy"),
    path("terminos/", views.terms_of_service, name="terms"),
]
