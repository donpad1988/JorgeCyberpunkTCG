from django.urls import path
from . import views
app_name="cards"
urlpatterns=[path("choomdex/",views.catalog,name="catalog"),path("choomdex/<slug:slug>/",views.detail,name="detail")]
