from django.http import HttpResponse
from django.views.generic.base import TemplateView


class CodegolfPageView(TemplateView):
  """Страница с codegolf"""

  template_name = 'index.html'

  def get_context_data(self, *args, **kwargs):
    context = super().get_context_data(*args, **kwargs)

    return context