from django.urls import path

from . import views

urlpatterns = [

    path("login/", views.login_request, name='login'),
    path("logout/", views.logoutUser, name='logout'),

    path("", views.MoviesView.as_view(), name="movie_list"),
    path("create_movie/", views.MovieCreate, name='create_movie'),
    path("<slug:slug>/", views.MoviesDetailView.as_view(), name="movie_detail"),
    path("update_movie/<slug:slug>/", views.updateMovie, name='update_movie'),
    path("delete_movie/<slug:slug>/", views.deleteMovie, name='delete_movie'),

]