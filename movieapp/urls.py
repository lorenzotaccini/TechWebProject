from django.urls import path

from .views import *

app_name = "movieapp"
urlpatterns = [
    path(r'', MovieListView.as_view(), name='home'),
    path('movie/<int:pk>/<int:page>/', MovieDetailView.as_view(), name='movie_detail'),
    path('movie/<int:pk>/', MovieDetailView.as_view(), name='movie_detail_nopage'),

    path('movie/<int:pk>/request/', create_request_ajax, name='create_request_ajax'),
    path('movie/<int:pk>/remove/', remove_request_ajax, name='remove_request_ajax'),
    path('movie/remove/', remove_request_ajax, name='remove_request_ajax_noparam'),
    path('watchlist/', add_movie_to_watchlist, name='add_movie_to_watchlist'),

    path('getrecommended/', title_recommendation, name='get_recommended_titles'),
    path('search/', SearchMovieListView.as_view(), name='search_title'),
    path('autocomplete/', MovieAutocomplete.as_view(), name='movie_autocomplete'),

]
