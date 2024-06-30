from django.contrib import admin

from movieapp.models import Movie, Profile, Request

# Register your models here.

admin.site.register(Movie)
admin.site.register(Profile)
admin.site.register(Request)
