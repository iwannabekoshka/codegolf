from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path("", views.CodegolfListView.as_view(), name="game_list"),
    path("<slug:pk>/", csrf_exempt(views.CodegolfPageView.as_view()), name="game_task"),
    path("<slug:pk>/get_scoreboard/", views.get_scoreboard, name="game_task"),
]