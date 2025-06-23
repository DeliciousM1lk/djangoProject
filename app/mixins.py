from django.http import JsonResponse
from django.views.generic.base import ContextMixin
from pyexpat.errors import messages

from .models import Rubric


class RubricMixin(ContextMixin):
    menu = [
        {'title': "Главная", 'url_name': 'app:all_class'},
        {'title': "Создать пост", 'url_name': 'app:create'},
        {'title': "Контакты", 'url_name': 'app:contact'},
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = self.menu
        context['rubric'] = Rubric.objects.all()
        return context


class JsonResponseMixin:
    def render_to_json_response(self, context, **response_kwargs):
        return JsonResponse(context, **response_kwargs)

class SuccessMessageMixin:
    success_message = ""

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.success_message:
            messages.success(self.request, self.success_message)
            print(f"Success message: {self.success_message}")
        return response