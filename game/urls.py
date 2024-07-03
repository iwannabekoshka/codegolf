from django.urls import path

from . import views

urlpatterns = [
    path("", views.CodegolfListView.as_view(), name="game_list"),
    path("<int:id>/", views.CodegolfPageView.as_view(), name="game_task"),
]