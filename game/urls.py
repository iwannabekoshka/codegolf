from django.urls import path

from . import views

urlpatterns = [
    path("", views.CodegolfPageView.as_view(), name="game_index"),
]