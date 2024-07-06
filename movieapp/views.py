from urllib.parse import urlparse

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, View
from django.views.generic import ListView

from .models import Profile, Request
from .workers import *


class MovieListView(ListView):
    model = Movie
    template_name = 'movie_list.html'
    paginate_by = 10


class SearchMovieListView(MovieListView):
    def get_queryset(self):
        query = self.request.GET.get('q')
        res = self.model.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
        if not res:  # try to catch mispelled infos
            similars = find_similar_movies(list(Movie.objects.values_list('title', flat=True)), query)
            return Movie.objects.filter(title__in=similars)
        if query:
            return res
        else:
            return Movie.objects.none()


class MovieAutocomplete(View):
    def get(self, request, *args, **kwargs):
        term = request.GET.get('term', '')
        movies = Movie.objects.filter(Q(title__icontains=term) | Q(description__icontains=term))[:10]
        suggestions = []
        if not movies:
            similar_titles = find_similar_movies(list(Movie.objects.values_list('title', flat=True)), term)
            movies = Movie.objects.filter(title__in=similar_titles)
        for movie in movies:
            suggestions.append({
                'label': f"{movie.title} ({movie.year})",
                'value': movie.title
            })
        return JsonResponse(suggestions, safe=False)


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
            if parsed_url.path.strip('/').split('/')[0] == 'movie':
                context['prev_page'] = reverse('movieapp:home')
            else:
                context['prev_page'] = self.request.META.get('HTTP_REFERER')
            context['back_btn'] = False
        user = self.request.user
        movie = self.get_object()
        # movie recommendation system is called, results added to context
        context['recommended_movies'] = title_recommendation(movie)
        if user.is_authenticated:
            user_profile = get_object_or_404(Profile, user=user)
            existing_request = Request.objects.filter(profile=user_profile, movie=movie).exists()
            context['existing_request'] = existing_request
            request_count = Request.objects.filter(movie=movie).count()
            context['request_count'] = request_count
            context['movie_request'] = Request.objects.filter(profile=user_profile, movie=movie).first()

        else:
            context['existing_request'] = False
        return context


@login_required
@require_POST
def create_request_ajax(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if not movie.available:
        profile = get_object_or_404(Profile, user=request.user)
        existing_request = Request.objects.filter(profile=profile, movie=movie).exists()

        if existing_request:
            print('request is somehow already existing... defuck?')
            return JsonResponse({'status': 'error', 'message': 'Request already exists.'}, status=400)
        else:
            new_request = Request(profile=profile, movie=movie)
            new_request.save()
            return JsonResponse({'status': 'success', 'message': 'Request sent successfully.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'You cannot request this movie because it is already '
                                                           'marked as available.'}, status=400)


@login_required
@require_POST
def remove_request_ajax(request, pk=None):
    if pk is None:
        pk = request.POST.get('movie_id')
    movie = get_object_or_404(Movie, pk=pk)

    profile = get_object_or_404(Profile, user=request.user)

    if Request.objects.filter(profile=profile, movie=movie).exists():
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
