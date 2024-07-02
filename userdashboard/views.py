from braces.views import GroupRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView

from movieapp.models import Request, Profile, Movie
# Create your views here.
from movieapp.views import MovieListView

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required(login_url='/login')
def my_watchlist(request):
    user_profile = request.user.profile
    watchlist_movies = user_profile.watchlisted.all()

    # Paginazione dei risultati con 10 elementi per pagina
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
    model = Request
    template_name = 'moderator_dashboard.html'
    paginate_by = 10
    ordering = ['-request_date']
