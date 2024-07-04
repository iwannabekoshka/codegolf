from django.db import models
from django.contrib.auth import get_user_model

from .constants import *


class Task(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    expected_output = models.TextField(verbose_name="Ожидаемый вывод", default='')
    example_code = models.TextField('Код примера', default='')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"


class Answer(models.Model):
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='answers', verbose_name="Задача"
    )
    code = models.TextField(verbose_name="Ответ")
    code_lang = models.CharField(
        max_length=255, verbose_name="Язык программирования", default='', null=True, choices=CODE_LANGUAGES
    )
    code_result = models.TextField('Результат', default='')
    code_len = models.PositiveIntegerField('Длина ответа', default=0)
    username = models.CharField('username', max_length=255, default='')
    is_correct = models.BooleanField('Ответ верен', default=False)

    def __str__(self):
        return f"{self.pk}"

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"
