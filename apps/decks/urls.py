from django.urls import path

from . import views

app_name = "decks"

urlpatterns = [
    path("mazos/", views.my_decks, name="my_decks"),
    path("mazos/publicos/", views.public_decks, name="public_decks"),
    path("mazos/crear/", views.deck_create, name="deck_create"),
    path("mazos/<str:username>/<slug:slug>/construir/", views.deck_builder, name="deck_builder"),
    path("mazos/<str:username>/<slug:slug>/editorial/", views.deck_editorial_update, name="deck_editorial_update"),
    path("mazos/<str:username>/<slug:slug>/legend/anadir/", views.legend_add, name="legend_add"),
    path("mazos/<str:username>/<slug:slug>/legend/retirar/", views.legend_remove, name="legend_remove"),
    path("mazos/<str:username>/<slug:slug>/main/anadir/", views.main_add, name="main_add"),
    path("mazos/<str:username>/<slug:slug>/main/decrementar/", views.main_decrement, name="main_decrement"),
    path("mazos/<str:username>/<slug:slug>/main/quitar/", views.main_remove, name="main_remove"),
    path("mazos/<str:username>/<slug:slug>/", views.deck_detail, name="deck_detail"),
    path("mazos/<str:username>/<slug:slug>/editar/", views.deck_update, name="deck_update"),
    path("mazos/<str:username>/<slug:slug>/eliminar/", views.deck_delete, name="deck_delete"),
]
