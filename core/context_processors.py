import datetime

from .models import *


def posts(request):
    return {'posts': Post.objects.all()}


def site_info(request):
    return {
        'site_name': "My Site Name",
        'site_description': "My Site Description",
        'site_ver': "1.0.0",
    }


def all_users(request):
    users = User.objects.all()

    return {
        'all_users': users
    }

def current_year(request):
    return {
        'current_year': datetime.datetime.now().year
    }