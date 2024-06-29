import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DetailView

from .forms import UpdateUserForm, UpdateProfileForm
from .models import Movie, Profile
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
