from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView
from .models import Post

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/home.html'


class PostListView(PermissionRequiredMixin, ListView):
    permission_required = "core.view_secret_post"
    model = Post
    template_name = "registration/post_list.html"


class PostCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "core.view_secret_post"
    model = Post
    template_name = "registration/post_create.html"
    fields = ['title', 'body']
    success_url = "core/posts/"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
