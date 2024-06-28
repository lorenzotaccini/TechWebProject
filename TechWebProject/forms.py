from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group


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
