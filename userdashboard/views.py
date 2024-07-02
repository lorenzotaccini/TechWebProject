from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView

from movieapp.models import Request, Profile
# Create your views here.
from movieapp.views import MovieListView


def my_watchlist(request):
    user_profile = request.user.profile
    watchlist_movies = user_profile.watchlisted.all()

    return render(request, 'watchlist.html', {'watchlist_movies': watchlist_movies})


class MyRequests(ListView):
    model = Request
    template_name = 'my_requests.html'

    def get_queryset(self):
        user_profile = get_object_or_404(Profile, user=self.request.user)
        return Request.objects.filter(profile=user_profile)
