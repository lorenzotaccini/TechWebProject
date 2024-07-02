import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import ListView, UpdateView, DetailView

from .forms import UpdateUserForm, UpdateProfileForm
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
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            user_profile = get_object_or_404(Profile, user=user)
            movie = self.get_object()
            existing_request = Request.objects.filter(profile=user_profile, movie=movie).exists()
            context['existing_request'] = existing_request
            request_count = Request.objects.filter(movie=movie).count()
            context['request_count'] = request_count
            context['movie_request'] = Request.objects.filter(profile=user_profile, movie=movie).first()
        else:
            context['existing_request'] = False
        return context


@login_required(login_url='/login')
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('movieapp:home')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required(login_url='/login')
@require_POST
def create_request_ajax(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    profile = get_object_or_404(Profile, user=request.user)
    existing_request = Request.objects.filter(profile=profile, movie=movie).exists()

    if existing_request:
        return JsonResponse({'status': 'error', 'message': 'Request already exists.'}, status=400)

    new_request = Request(profile=profile, movie=movie)
    new_request.save()
    print(movie)
    return JsonResponse({'status': 'success', 'message': 'Request sent successfully.'})


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
