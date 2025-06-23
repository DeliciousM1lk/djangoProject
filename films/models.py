from django.db import models

class Actor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Film(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    year = models.DateField()
    actors = models.ManyToManyField(Actor, related_name="films")

    def __str__(self):
        return self.name
