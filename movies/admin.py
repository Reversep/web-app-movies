from django.contrib import admin

from .models import Category, Genre, Movie, MovieShots, Actor

admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(MovieShots)
admin.site.register(Actor)

