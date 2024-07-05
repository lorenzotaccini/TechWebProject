from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from .forms import *
from django.contrib.auth import login, logout, authenticate
from braces.views import GroupRequiredMixin, SuperuserRequiredMixin

class UserCreateView(CreateView):
    form_class = CreateRegisteredUserForm
    template_name = "user_create.html"
    success_url = reverse_lazy("login")


class ModeratorCreateView(SuperuserRequiredMixin, CreateView):
    form_class = CreateModeratorForm
    template_name = "moderator_create.html"
    success_url = reverse_lazy("movieapp:home")


def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        redirect_to = request.GET.get('next', '')
        print(redirect_to)
        if user is not None:
            login(request, user)
            if redirect_to:
                return HttpResponseRedirect(redirect_to)
            #messages.success(request, f"Hi {username}, you are now logged in! Welcome back.")
            return redirect('/?login=ok')
        else:
            #messages.error(request, "There was an error logging in... Please try again.")
            return render(request, 'login_user.html', context={'error_msg': "Login failed. Check username and password."})

    else:
        return render(request, "login_user.html")


def logout_user(request):
    logout(request)
    #messages.success(request, "You have been logged out. See you soon.")
    return redirect('/?logout=ok')

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES or None, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('movieapp:home')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})
