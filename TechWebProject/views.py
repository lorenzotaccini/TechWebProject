from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import *

class UserCreateView(CreateView):
    #form_class = UserCreationForm
    form_class = CreateRegisteredUserForm
    template_name = "user_create.html"
    success_url = reverse_lazy("login")
