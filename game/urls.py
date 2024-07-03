from django.urls import path

from . import views

urlpatterns = [
    path("", views.CodegolfListView.as_view(), name="game_list"),
    path("<slug:pk>/", views.CodegolfPageView.as_view(), name="game_task"),
]