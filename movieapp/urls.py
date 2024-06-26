from django.urls import path
from .views import testview, TestClassView

urlpatterns = [
    path('', testview, name='index'),
    path('list/', TestClassView.as_view(), name='list'),
]
