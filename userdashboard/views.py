from braces.views import GroupRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView

from movieapp.models import Request, Profile, Movie
# Create your views here.
from movieapp.views import MovieListView

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required(login_url='/login')
def user_dashboard(request):
    return render(request, 'user_dashboard.html')


@login_required(login_url='/login')
def my_watchlist(request):

    user_profile = request.user.profile
    watchlist_movies = user_profile.watchlisted.all()

    # Paginazione dei risultati con 5 elementi per pagina
    paginator = Paginator(watchlist_movies, 5)
    page_number = request.GET.get('page')

    try:
        watchlist_movies = paginator.page(page_number)
    except PageNotAnInteger:
        watchlist_movies = paginator.page(1)
    except EmptyPage:
        watchlist_movies = paginator.page(paginator.num_pages)

    return render(request, 'watchlist.html', {'watchlist_movies': watchlist_movies})


class MyRequests(LoginRequiredMixin, ListView):
    model = Request
    template_name = 'my_requests.html'
    context_object_name = 'requests'
    paginate_by = 5

    def get_queryset(self):
        user_profile = get_object_or_404(Profile, user=self.request.user)
        return Request.objects.filter(profile=user_profile).all()


class ModeratorDashboard(GroupRequiredMixin, ListView):
    group_required = 'Moderator'
    model = Movie
    template_name = 'moderator_dashboard.html'
    paginate_by = 5

    def get_queryset(self):
        # Seleziona solo i film per cui esiste almeno una Request
        return Movie.objects.filter(requested_by__isnull=False).distinct()


def is_moderator_or_higher(user):
    return user.groups.filter(name='Moderator').exists() or user.is_superuser



@user_passes_test(is_moderator_or_higher)
@require_POST
def manage_requested_title(request):
    action = request.POST.get('action')
    movie = get_object_or_404(Movie, tmdb_id=request.POST['movie_id'])
    if action == 'approve':
        movie.movie_requests.all().update(status='approved')
        print('approved')
    elif action == 'reject':
        movie.movie_requests.all().update(status='rejected')
        print('rejected')
    elif action == 'mark_available':
        movie.available = True
        movie.save()
        print('marked available')
    return JsonResponse({'status': 'ok'})

