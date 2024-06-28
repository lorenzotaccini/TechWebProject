from django.contrib import admin

from movieapp.models import Movie, Profile

# Register your models here.

admin.site.register(Movie)
admin.site.register(Profile)