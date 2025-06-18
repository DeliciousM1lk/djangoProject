from django.forms import *
from .models import *


class BbForm(ModelForm):
    class Meta:
        model = Bb
        fields = ['rubric','title','content','price']

class ContactForm(forms.Form):
    name=CharField(label="Имя",max_length=100)
    email=EmailField(label="Email")
    text=CharField(label="Сообщение",max_length=500,widget=Textarea)


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

class RubricBaseFormSet(BaseModelFormSet):
    def clean(self):
        super().clean()

        names = [
            form.cleaned_data.get("name")
            for form in self.forms
            if form.cleaned_data and not form.cleaned_data.get("DELETE")
        ]

        required = {"Недвижимость", "Авто"}
        missing = required - set(names)

        if missing:
            raise ValidationError(
                f"Добавьте рубрики: {', '.join(sorted(missing))}"
            )



class QuestionInline(BaseInlineFormSet):
    MIN_QUESTIONS = 2
    MAX_QUESTIONS = 10

    def clean(self):
        super().clean()

        alive=len(self.forms) - len(self.deleted_forms)
        if alive < self.MIN_QUESTIONS:
            raise ValidationError(f"Минимальное количество вопросов: {self.MIN_QUESTIONS}")

        if alive > self.MAX_QUESTIONS:
            raise ValidationError(f"Максимальное количество вопросов: {self.MAX_QUESTIONS}")

QuestionFormSet= inlineformset_factory(
    Quiz,
    Question,
    fields=('text',),
    formset=QuestionInline,
    extra=3,
    can_delete=True
)



