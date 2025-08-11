from django.views.generic.base import ContextMixin
from .models import Film


class GenreListMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Film.objects.values_list('genre', flat=True).distinct()
        return context