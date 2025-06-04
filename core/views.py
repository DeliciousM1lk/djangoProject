from cmath import acosh

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/home.html'
