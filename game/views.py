from django.http import JsonResponse
from django.shortcuts import get_object_or_404, Http404, render
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView

import json

from .models import Task, Answer


class CodegolfListView(ListView):
  """Страница со списком заданий"""

  model = Task
  template_name = 'list.html'


class CodegolfPageView(DetailView):
  """Страница задания"""

  model = Task
  template_name = 'id.html'
  context_object_name = 'task'

  def post(self, request, *args, **kwargs):
    self.object = self.get_object()
    data = json.loads(request.body.decode('utf-8'))
    answer_text = data.get('code')

    if not answer_text:
      return JsonResponse({'status': 'error', 'message': 'Отсутствуют необходимые данные'}, status=400)

    answer = Answer(task=self.object, answer_text=answer_text)
    answer.save()

    return JsonResponse({
      'status': 'success', 
      'message': 'Ответ успешно создан',
      'expectedOutput': self.object.expected_output,
      'userOutput': answer_text
    })
