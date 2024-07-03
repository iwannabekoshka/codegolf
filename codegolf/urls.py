from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path("game/", include("game.urls")),
    path("admin/", admin.site.urls),
]