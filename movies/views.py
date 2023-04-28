from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.db.models.functions import Lower


from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.views.generic.base import View
from .models import Movie, Category, Genre
from .forms import MovieForm


class GenreYear:

    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values("year")


class MoviesView(GenreYear, View):
    def get(self, request):
        movies = Movie.objects.all()
        return render(request, 'movies/movie_list.html', {"movies": movies})


class MoviesDetailView(GenreYear, View):
    def get(self, request, slug):
        try:
            movies = Movie.objects.get(url=slug)
        except:
            movies = None
        return render(request, 'movies/movie_detail.html', {'movies': movies})

@login_required()
def MovieCreate(request):
    form = MovieForm()
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print(form.errors)
            return redirect('/')
        else:
            print(form.errors)

    context = {'form': form}
    return render(request, 'movie_forms.html', context)

@login_required()
def updateMovie(request, slug):
    movies = Movie.objects.get(url=slug)
    form = MovieForm(instance=movies)
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movies)
        if form.is_valid():
            form.save()
            print(form.errors)
            return redirect('/')
        else:
            print(form.errors)
    context = {'form': form}
    return render(request, 'movie_forms.html', context)


# def deleteMovie(request, slug):
#     try:
#         movies = Movie.objects.get(url=slug)
#     except:
#         movies = None
#
#     if request.method == 'POST':
#         movies.delete()
#         return redirect('/')
#     context = {'item': movies}
#     return render(request, 'delete.html', context)

@login_required()
def deleteMovie(request, slug):
    try:
        movies = Movie.objects.get(url=slug)
    except Movie.DoesNotExist:
        movies = None

    if request.method == 'POST' and movies:
        movies.delete()
        return redirect('movie_list')
    context = {'item': movies}
    return render(request, 'delete.html', context)


# def loginPage(request):
#
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#
#         if user is not None:
#             login(request, user)
#             return redirect('/')
#
#     context = {}
#     return render(request, 'login.html', context)


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("movie_list")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form": form})


@login_required()
def logoutUser(request):
    logout(request)
    return redirect('/')


def search(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        movies = Movie.objects.filter(title__icontains=query)
        return render(request, 'dashboard.html', {'movies': movies})
    else:
        return render(request, 'dashboard.html')



