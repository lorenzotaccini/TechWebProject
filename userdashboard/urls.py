from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.contrib.auth import login,logout, authenticate
from . import views

app_name= "userdashboard"

urlpatterns = [
    path('watchlist/', views.my_watchlist, name='my_watchlist'),
]
