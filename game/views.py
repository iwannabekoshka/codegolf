from django.http import JsonResponse
from django.shortcuts import get_object_or_404, Http404, render
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from django.template.loader import render_to_string

import json

from .models import Task, Answer, CODE_LANGUAGES
from .utils import execute_cpp_code


class CodegolfListView(ListView):
  """Страница со списком заданий"""

  model = Task
  template_name = 'list.html'


class CodegolfPageView(DetailView):
  """Страница задания"""

  model = Task
  template_name = 'id.html'
  context_object_name = 'task'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    context.update({
      'code_languages': CODE_LANGUAGES
    })

    return context

  def post(self, request, *args, **kwargs):
    data = json.loads(request.body.decode('utf-8'))
    code = data.get('code')
    code_lang = data.get('code_lang')

    # if not code:
    #   return JsonResponse({'status': 'error', 'message': 'Отсутствуют необходимые данные'}, status=400)

    exec_data = execute_cpp_code(code)
    if 'error' in exec_data:
      response = {
        'status': 'error',
        'message': f"{exec_data['error']}: {exec_data['details']}"
      }
    else:
      response = {
        'status': 'success',
        'message': 'Ответ успешно создан',
        'userOutput': exec_data['output']
      }
    response.update({
      'expectedOutput': self.get_object().expected_output,
    })
    #answer = Answer(task=self.get_object(), code=code, code_lang=code_lang)
    #answer.save()

    return JsonResponse(response)

def get_scoreboard(request, pk):
  rows = [
    {'username': 'ABOBA', 'code_len': '1'},
    {'username': 'abeba', 'code_len': '10'},
    {'username': 'bobster', 'code_len': '11'},
    # Добавьте другие строки по необходимости
  ]

  html_content = render_to_string('table_rows.html', {'rows': rows})

  return JsonResponse({'html': html_content})