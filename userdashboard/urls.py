from django.urls import path

from .views import *

app_name = "userdashboard"

urlpatterns = [
    path('watchlist/', my_watchlist, name='my_watchlist'),
    path('myrequests/', MyRequests.as_view(), name='my_requests'),
    path('moderatordashboard/', ModeratorDashboard.as_view(), name='moderator_dashboard'),
    path('userdashboard/', user_dashboard, name='user_dashboard'),

    path('managerequest/', manage_requested_title, name='manage_requested_title'),

    path('addtitle/', add_title, name='add_new_title'),

]


