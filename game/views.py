from django.http import HttpResponse
from django.views.generic.base import TemplateView

class CodegolfPageView(TemplateView):
  """Страница с codegolf"""

  template_name = 'index.html'

  def get_context_data(self, *args, **kwargs):
    context = super().get_context_data(*args, **kwargs)

    context.update({
      'task_id': 1,
      'task_title': '99 Bottles of Beer',
      'task_description': f"Print the lyrics to the song 99 Bottles of Beer:<br>99 bottles of beer on the wall, 99 bottles of beer.Take one down and pass it around, 98 bottles of beer on the wall.<br>98 bottles of beer on the wall, 98 bottles of beer.Take one down and pass it around, 97 bottles of beer on the wall.<br>…<br>1 bottle of beer on the wall, 1 bottle of beer.Take one down and pass it around, no more bottles of beer on the wall.<br>No more bottles of beer on the wall, no more bottles of beer.Go to the store and buy some more, 99 bottles of beer on the wall.",
    })

    return context