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


class Answer(models.Model):
  task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='answers')
  answer_text = models.TextField()

  def __str__(self):
    return f"{self.pk}"
