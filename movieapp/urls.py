from django.urls import path
from django.views.generic import TemplateView

from .views import MovieListView

app_name = "movieapp"
urlpatterns = [
    path(r'', MovieListView.as_view(), name='home'),
    #path('title/<pk>')
]
