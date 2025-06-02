from django.forms import *
from .models import *


class BbForm(ModelForm):
    class Meta:
        model = Bb
        fields = ['rubric', 'title', 'content', 'price']

        labels = {
            'rubric': 'Рубрика',
            'title': 'Заголовок',
            'content': 'Описание',
            'price': 'Цена',
        }

        help_texts = {
            'rubric': 'Выберите подходящую рубрику для вашего объявления.',
            'title': 'Введите краткий и понятный заголовок.',
            'content': 'Подробно опишите товар или услугу.',
            'price': 'Укажите цену в тенге.',
        }

        widgets = {
            'rubric': Select(attrs={'class': 'form-select'}),
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите заголовок'}),
            'content': Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Введите описание'}),
            'price': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Цена'}),
        }


class ContactForm(forms.Form):
    name = CharField(label="Имя", max_length=100)
    email = EmailField(label="Email")
    text = CharField(label="Сообщение", max_length=500, widget=Textarea)


BbFormFactory = modelform_factory(
    Bb,
    fields=['rubric', 'title', 'content', 'price'],
    widgets={
        'rubric': Select(attrs={'class': 'form-select'}),
        'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите заголовок'}),
        'content': Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Введите описание'}),
        'price': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Цена'}),
    },
    labels={
        'rubric': 'Рубрика',
        'title': 'Заголовок',
        'content': 'Описание',
        'price': 'Цена',
    },
    help_texts={
        'rubric': 'Выберите подходящую рубрику для вашего объявления.',
        'title': 'Введите краткий и понятный заголовок.',
        'content': 'Подробно опишите товар или услугу.',
        'price': 'Укажите цену в тенге.',
    }
)


class RubricForm(ModelForm):
    class Meta:
        model = Rubric
        fields = ['name']
        labels = {
            'name': 'Название рубрики'
        }
        help_texts = {
            'name': 'Введите название рубрики'
        }
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Название рубрики'})
        }


RubricFormSet = modelformset_factory(
    Rubric,
    form=RubricForm,
    can_delete=True,
    extra=2
)
