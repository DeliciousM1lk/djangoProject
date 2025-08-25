from django.db import models
from django.contrib.postgres.fields import ArrayField, HStoreField
from django.contrib.postgres.fields.citext import CICharField


class Film(models.Model):
    slug = models.SlugField(unique=True, blank=False, null=False)
    name = models.CharField(max_length=100, null=False, blank=False)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    year = models.DateField(null=False, blank=False)

    tags = ArrayField(
        models.CharField(max_length=50),
        size=5,
        blank=True,
        default=list,
        help_text="Список тегов к фильму"
    )

    metadata = HStoreField(
        blank=True,
        null=True,
        help_text="Произвольные пары ключ=значение"
    )

    ci_title = CICharField(
        max_length=100,
        unique=True,
        help_text="Название без учёта регистра"
    )

    def __str__(self):
        return self.name
