from django.http import HttpResponse
from django.shortcuts import get_object_or_404, Http404, render
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView

from .models import Task


class CodegolfListView(ListView):
  """Страница со списком заданий"""

  model = Task
  template_name = 'list.html'

  def get_context_data(self, *args, **kwargs):
    context = super().get_context_data(*args, **kwargs)

    return context


class CodegolfPageView(DetailView):
  """Страница задания"""

  model = Task
  template_name = 'id.html'
  context_object_name = 'task'