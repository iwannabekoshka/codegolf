from django.db import models

class Task(models.Model):
  title = models.CharField(max_length=255, verbose_name="Название")
  description = models.TextField(verbose_name="Описание")
  expected_output = models.TextField(verbose_name="Ожидаемый вывод")

  def __str__(self):
    return self.title

  class Meta:
    verbose_name = "Задача"
    verbose_name_plural = "Задачи"


CODE_LANGUAGES = (
  ('cpp', 'C++'),
)
class Answer(models.Model):
  task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='answers', verbose_name="Задача")
  code = models.TextField(verbose_name="Ответ")
  code_lang = models.CharField(max_length=255, verbose_name="Язык программирования", default=None, null=True, choices=CODE_LANGUAGES)

  def __str__(self):
    return f"{self.pk}"

  class Meta:
    verbose_name = "Ответ"
    verbose_name_plural = "Ответы"
