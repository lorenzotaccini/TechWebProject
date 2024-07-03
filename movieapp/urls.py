from django.urls import path, re_path
from django.views.generic import TemplateView

from .views import MovieListView, profile, MovieDetailView, create_request_ajax, add_movie_to_watchlist, remove_request_ajax

app_name = "movieapp"
urlpatterns = [
    path(r'', MovieListView.as_view(), name='home'),
    path('movie/<int:pk>/<int:page>/', MovieDetailView.as_view(), name='movie_detail'),
    path('edit_profile/', profile, name='edit_profile'),
    path('movie/<int:pk>/request/', create_request_ajax, name='create_request_ajax'),
    path('movie/<int:pk>/remove/', remove_request_ajax, name='remove_request_ajax'),
    path('movie/remove/', remove_request_ajax, name='remove_request_ajax_noparam'),
    path('watchlist/', add_movie_to_watchlist, name='add_movie_to_watchlist'),

]
