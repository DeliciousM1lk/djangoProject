from django.forms import *
from .models import *


class FilmForm(ModelForm):
    class Meta:
        model = Film
        fields = ['slug','name','genre','author','year']

