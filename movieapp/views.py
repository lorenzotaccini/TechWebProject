from django.http import HttpResponse
from django.shortcuts import render
from django.forms import ModelForm
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from .models import Movie

def testview(request):
    return HttpResponse("Hello World")


class TestClassView(ListView):
    model = Movie
    template_name = 'movie_list.html'
    paginate_by = 10
