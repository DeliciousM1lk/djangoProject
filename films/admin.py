from django.contrib import admin
from .models import *

@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'genre', 'year')
    list_display_links = ('name',)
    search_fields = ('name', 'author',)
    ordering = ('year',)
    list_filter = ('genre', 'year',)
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('year',)
