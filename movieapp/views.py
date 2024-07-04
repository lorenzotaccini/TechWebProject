from urllib.parse import urlparse

import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.decorators.http import require_POST, require_GET
from django.views.generic import ListView, UpdateView, DetailView

from .models import Movie, Profile, Request
from django.views.generic import ListView

from .models import Movie


class MovieListView(ListView):
    model = Movie
    template_name = 'movie_list.html'
    paginate_by = 5


class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movie_detail.html'

    def get_my_page(self):
        return self.kwargs.get('page')

    def get_context_data(self, **kwargs):
        parsed_url = urlparse(self.request.META.get('HTTP_REFERER'))
        context = super().get_context_data(**kwargs)
        if parsed_url.path == '/':
            context['back_btn'] = True
        else:
            context['back_btn'] = False
            context['prev_page'] = self.request.META.get('HTTP_REFERER')
        user = self.request.user
        if user.is_authenticated:
            user_profile = get_object_or_404(Profile, user=user)
            movie = self.get_object()
            existing_request = Request.objects.filter(profile=user_profile, movie=movie).exists()
            context['existing_request'] = existing_request
            request_count = Request.objects.filter(movie=movie).count()
            context['request_count'] = request_count
            context['movie_request'] = Request.objects.filter(profile=user_profile, movie=movie).first()

            #movie recommendation system is called, results added to context
            context['recommended_movies'] = title_recommendation(movie)

        else:
            context['existing_request'] = False
        return context


def title_recommendation(movie: Movie):

    def count_common_genres(list1, list2):
        return len(set(list1) & set(list2))

    genres = movie.get_genre_as_list()
    print('retrieved list is {}'.format(genres))
    allmovies_genre_list = [(m, m.get_genre_as_list()) for m in
                            Movie.objects.all().exclude(tmdb_id=movie.tmdb_id)]
    print(allmovies_genre_list)
    common_genres_list = [[elem[0], count_common_genres(genres, elem[1])] for elem in allmovies_genre_list]
    common_genres_list = sorted(common_genres_list, key=lambda x: x[1], reverse=True)
    print(common_genres_list)
    recommended_titles = [elem[0] for elem in common_genres_list if elem[1]][:5]
    print(recommended_titles)
    if len(recommended_titles) > 0:
        return recommended_titles
    else:
        return None


@login_required(login_url='/login')
@require_POST
def create_request_ajax(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if not movie.available:
        profile = get_object_or_404(Profile, user=request.user)
        existing_request = Request.objects.filter(profile=profile, movie=movie).exists()

        if existing_request:
            return JsonResponse({'status': 'error', 'message': 'Request already exists.'}, status=400)

        new_request = Request(profile=profile, movie=movie)
        new_request.save()
        print(movie)
        return JsonResponse({'status': 'success', 'message': 'Request sent successfully.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'You cannot request this movie because it is already '
                                                           'marked as available.'}, status=400)


@login_required(login_url='/login')
@require_POST
def remove_request_ajax(request, pk=None):
    if pk is None:
        pk = request.POST.get('movie_id')
        print(pk)
    movie = get_object_or_404(Movie, pk=pk)
    print('movie is' + str(movie))
    profile = get_object_or_404(Profile, user=request.user)

    if Request.objects.filter(profile=profile, movie=movie).exists():
        print('removed movie')
        profile.requests.remove(movie)
        return JsonResponse({'status': 'success', 'message': 'Request removed successfully.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Trying to remove a request that doesn\'t exists'},
                            status=400)


@require_POST
@login_required
def add_movie_to_watchlist(request):
    movie = get_object_or_404(Movie, tmdb_id=request.POST.get('movie_id'))
    user_profile = get_object_or_404(Profile, user=request.user)
    if user_profile.watchlisted.filter(tmdb_id=request.POST.get('movie_id')).exists():
        user_profile.watchlisted.remove(movie)
        return JsonResponse({'status': 'ok'})
    else:
        user_profile.watchlisted.add(movie)
        return JsonResponse({'status': 'ok'})
