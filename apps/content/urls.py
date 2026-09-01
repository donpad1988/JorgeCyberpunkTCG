from django.urls import path

from . import views

app_name = "content"

urlpatterns = [
    path("guias/", views.guide_list, name="guide_list"),
    path("guias/<slug:slug>/", views.guide_detail, name="guide_detail"),
    path("estrategias/", views.strategy_list, name="strategy_list"),
    path("estrategias/<slug:slug>/", views.strategy_detail, name="strategy_detail"),
]
