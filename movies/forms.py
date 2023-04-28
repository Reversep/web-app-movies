from django import forms
from .models import Category, Actor, Genre, Movie, MovieShots
from django.forms import ModelForm


class MovieForm(ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'
