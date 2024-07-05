from django.db import connection
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, Http404, render
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from django.template.loader import render_to_string
from django.db.models import F, Window
from django.db.models.functions import RowNumber

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
        try:
            code = data['code']
            code_lang = data['code_lang']
            username = data['username']
            code_len = data['code_len']
        except KeyError:
            return JsonResponse({'status': 'error', 'message': 'Отсутствуют необходимые данные'}, status=400)

        task_obj = self.get_object()

        exec_data = execute_cpp_code(code)
        if 'error' in exec_data:
            response = {
                'status': 'error',
                'userOutput': f"{exec_data['error']}: {exec_data['details']}"
            }
        else:
            output = exec_data['output'].replace('\r\n', '\n').strip()
            expected_output = task_obj.expected_output.replace('\r\n', '\n').strip()
            is_correct = output == expected_output
            answer = Answer.objects.create(
                task=task_obj,
                code=code,
                code_lang=code_lang,
                code_result=output,
                username=username,
                is_correct=is_correct,
                code_len=code_len,
            )
            response = {
                'status': 'success',
                'userOutput': output,
                'is_correct': is_correct,
            }
        response.update({
            'expectedOutput': task_obj.expected_output,
        })

        return JsonResponse(response)


def get_scoreboard(request, pk):
    top_5 = [
        {'username': 'ABOBA', 'code_len': '1'},
        {'username': 'abeba', 'code_len': '10'},
        {'username': 'bobster', 'code_len': '11'},
        # Добавьте другие строки по необходимости
      ]

    query = '''
        SELECT id, username, MIN(code_len) as code_len
        FROM game_answer
        WHERE code_len > 0
        GROUP BY username
        ORDER BY code_len
        LIMIT 5
    '''

    answers = Answer.objects.raw(query)

    top_5 = [{'username': answer.username, 'code_len': answer.code_len} for answer in answers]

    html_content = render_to_string('table_rows.html', {'rows': top_5})
    print(top_5, '||')
    return JsonResponse({'html': html_content})
