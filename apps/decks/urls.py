from django.urls import path

from . import views

app_name = "decks"

urlpatterns = [
    path("mazos/", views.my_decks, name="my_decks"),
    path("mazos/publicos/", views.public_decks, name="public_decks"),
    path("mazos/crear/", views.deck_create, name="deck_create"),
    path("mazos/<str:username>/<slug:slug>/", views.deck_detail, name="deck_detail"),
    path("mazos/<str:username>/<slug:slug>/editar/", views.deck_update, name="deck_update"),
    path("mazos/<str:username>/<slug:slug>/eliminar/", views.deck_delete, name="deck_delete"),
]
