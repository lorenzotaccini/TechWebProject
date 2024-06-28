from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import *
from django.contrib.auth import login, logout, authenticate
from braces.views import GroupRequiredMixin

class UserCreateView(CreateView):
    #form_class = UserCreationForm
    form_class = CreateRegisteredUserForm
    template_name = "user_create.html"
    success_url = reverse_lazy("login")

class ModeratorCreateView(GroupRequiredMixin,CreateView):
    #form_class = UserCreationForm
    group_required = "Moderator"
    form_class = CreateRegisteredUserForm
    template_name = "user_create.html"
    success_url = reverse_lazy("login")

def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Hi {username}, you are now logged in! Welcome back.")
            return redirect('/?login=ok')
        else:
            messages.error(request, "There was an error logging in... Please try again.")
            return redirect('login')

    else:
        return render(request, "login_user.html")


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out. See you soon.")
    return redirect('/?logout=ok')
