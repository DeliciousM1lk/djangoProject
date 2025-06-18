from django.urls import *
from .views import *
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('posts/',PostListView.as_view(),name='post_list'),
    path('posts/new/',PostCreateView.as_view(),name='post_create'),
]


