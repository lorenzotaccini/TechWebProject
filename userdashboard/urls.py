from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.contrib.auth import login,logout, authenticate
from .views import my_watchlist,MyRequests,ModeratorDashboard,user_dashboard

app_name = "userdashboard"

urlpatterns = [
    path('watchlist/', my_watchlist, name='my_watchlist'),
    path('myrequests/', MyRequests.as_view(), name='my_requests'),
    path('moderatordashboard/', ModeratorDashboard.as_view(), name='moderator_dashboard'),
    path('userdashboard/', user_dashboard, name='user_dashboard')
]
