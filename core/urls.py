from django.urls import *
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]
