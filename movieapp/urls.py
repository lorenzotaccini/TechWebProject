from django.urls import path
from django.views.generic import TemplateView

from .views import MovieListView, profile, MovieDetailView, request_movie

app_name = "movieapp"
urlpatterns = [
    path(r'', MovieListView.as_view(), name='home'),
    path('movie/<int:pk>/<int:page>', MovieDetailView.as_view(), name='movie_detail'),
    path('edit_profile/', profile, name='edit_profile'),
    path('request_movie/<int:movie_id>/<int:prev_page>', request_movie, name='request_movie'),

]
