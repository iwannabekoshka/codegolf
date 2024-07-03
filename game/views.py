from django.http import HttpResponse
from django.shortcuts import get_object_or_404, Http404, render
from django.views.generic.base import TemplateView

from .models import Task

class CodegolfPageView(TemplateView):
  """Страница с codegolf"""

  template_name = 'index.html'

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