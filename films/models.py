from django.db import models


class Actor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class BaseContent(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class MediaContent(BaseContent):
    author = models.CharField(max_length=100)
    year = models.DateField()

    class Meta:
        abstract = True


class Film(MediaContent):
    actors = models.ManyToManyField(Actor, related_name="films")
    duration_minutes = models.PositiveIntegerField()

    def get_type(self):
        return "Фильм"


class Series(MediaContent):
    episodes = models.PositiveIntegerField()
    seasons = models.PositiveIntegerField()
    actors = models.ManyToManyField(Actor, related_name="series")

    def get_type(self):
        return "Сериал"
