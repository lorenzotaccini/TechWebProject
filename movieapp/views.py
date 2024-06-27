import requests
from django.views.generic import ListView
from .models import Movie
from django.views.generic import ListView

from .models import Movie


class MovieListView(ListView):
    model = Movie
    template_name = 'movie_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Titolo Dinamico della Lista'
        context['movie_list'] = Movie.objects.all()
        return context

