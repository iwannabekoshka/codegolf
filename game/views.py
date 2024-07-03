from django.http import HttpResponse
from django.shortcuts import get_object_or_404, Http404, render
from django.views.generic.base import TemplateView
from django.views.generic import ListView

from .models import Task


class CodegolfListView(ListView):
  """Страница с codegolf"""

  model = Task
  template_name = 'list.html'

  def get_context_data(self, *args, **kwargs):
    context = super().get_context_data(*args, **kwargs)

    return context


class CodegolfPageView(TemplateView):
  """Страница с codegolf"""

  template_name = 'id.html'

  def get_context_data(self, *args, **kwargs):
    context = super().get_context_data(*args, **kwargs)

    task = get_object_or_404(
      Task,
      id=kwargs.get('id'),
    )

    context.update({
      'task_id': task.id,
      'task_title': task.title,
      'task_description': task.description,
    })

    return context