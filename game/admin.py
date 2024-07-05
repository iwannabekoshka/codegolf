from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Task, Answer

@admin.register(Answer)
class AnswerAdmin(ModelAdmin):
    list_display = ('task', 'username', 'code_len', 'is_correct')
    list_filter = ('is_correct',)

admin.site.register(Task)
