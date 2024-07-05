from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path("", views.CodegolfListView.as_view(), name="game_list"),
    path("<int:pk>/", csrf_exempt(views.CodegolfPageView.as_view()), name="game_task"),
    path("<int:pk>/get_scoreboard/", views.get_scoreboard, name="game_task"),
]