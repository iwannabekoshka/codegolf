from django.urls import path

from . import views

urlpatterns = [
    path("<int:id>/", views.CodegolfPageView.as_view(), name="game_task"),
]