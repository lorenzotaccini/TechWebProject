from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group
from django import forms
from django.contrib.auth.models import User
from movieapp.models import Profile, Request



class CreateModeratorForm(UserCreationForm):
    def save(self, commit=True):
        user = super().save(commit)
        g = Group.objects.get(name="Moderator")
        g.user_set.add(user)
        return user


class CreateRegisteredUserForm(UserCreationForm):

    def save(self, commit=True):
        user = super().save(commit)
        g = Group.objects.get(name="Registered")
        g.user_set.add(user)
        return user


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['username','email']


class UpdateProfileForm(forms.ModelForm):
    propic = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))

    class Meta:
        model = Profile
        fields = ['propic']
