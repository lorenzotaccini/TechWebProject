from django.shortcuts import render
from django.views.generic import DetailView

# Create your views here.
from movieapp.views import MovieListView


class WatchlistedMovies(MovieListView):
    pass


class MyRequests(DetailView):
    pass
