import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DetailView

from .forms import UpdateUserForm, UpdateProfileForm
from .models import Movie, Profile, Request
from django.views.generic import ListView

from .models import Movie


class MovieListView(ListView):
    model = Movie
    template_name = 'movie_list.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Titolo Dinamico della Lista'
        context['movie_list'] = Movie.objects.all()
        return context


class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movie_detail.html'

    def get_my_page(self):
        return self.kwargs.get('page')

    def already_requested_by_user(self) -> bool:
        return Request.objects.filter(pk=self.kwargs.get('pk')).exists()

    @login_required
    def post(self, request, *args, **kwargs):
        # Recupera il film dalla tabella Movie
        movie = get_object_or_404(Movie, pk=self.kwargs.get('tmdb_id'))
        print(movie)
        # Recupera il profilo dell'utente loggato
        user_profile = Profile.objects.get(pk=self.kwargs.get('pk'))
        print(user_profile)

        if not Request.objects.filter(profile=profile, movie=movie).exists():
            movie_request = Request.objects.create(profile=user_profile, movie=movie)
            movie_request.save()
            print(f'Movie {movie} request has been successfully submitted!')
            print(request.path_info)
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            return render(request, 'movie_detail.html', {'already_requested': True})




@login_required
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

'''
@login_required
def request_movie(request, movie_id, prev_page):
    # Recupera il film dalla tabella Movie
    movie = get_object_or_404(Movie, pk=movie_id)
    # Recupera il profilo dell'utente loggato
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST' and not Request.objects.filter(profile=profile, movie=movie).exists():
        # Crea una nuova richiesta
        movie_request = Request.objects.create(profile=profile, movie=movie)
        movie_request.save()
        print(f'Movie {movie_id} request has been successfully submitted!')
        print(request.path_info)
        return render()
    else:
        # esiste già una request da parte di questo utente per questo film
        pass


    return redirect('movieapp:movie_detail', pk=movie.tmdb_id, page=prev_page)
'''