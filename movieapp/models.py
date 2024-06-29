from os.path import join

import requests
from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Movie(models.Model):
    tmdb_id = models.IntegerField(primary_key=True)  # useful to retrieve data from TMDB APIs
    title = models.CharField(max_length=100)
    year = models.IntegerField(null=True)
    description = models.TextField(max_length=1000)
    genre = models.CharField(max_length=100)
    available = models.BooleanField(default=False)

    @property
    def poster_url(self):
        api_key = '5dbf33ab1210565bba9d880c176bf3d8'
        base_url = f'https://api.themoviedb.org/3/movie/{self.tmdb_id}?api_key={api_key}'

    '''
        try:
            response = requests.get(base_url)
            data = response.json()

            if 'poster_path' in data and data['poster_path']:
                poster_path = data['poster_path']
                poster_url = f'https://image.tmdb.org/t/p/w154{poster_path}'
                return poster_url
            else:
                return None

        except requests.exceptions.RequestException as e:
            print('Error in API request:', e)
            return None
    '''

    def __str__(self):
        return f"{self.title} - {self.tmdb_id}"

    class Meta:
        ordering = ["-pk"]
        verbose_name_plural = 'Movies'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    propic = models.ImageField(
        upload_to='users_pics',
        default=join('static', 'unknown_user.png'),
        blank=True
    )
    requests = models.ManyToManyField(Movie, through='Request', blank=True, related_name='requests', default=None)
    watchlisted = models.ManyToManyField(Movie, blank=True, related_name='watchlisted', default=None)

    def __str__(self):
        return f"{self.user.pk} - {self.user.username}"


class Request(models.Model):
    APPROVED = 'approved'
    REJECTED = 'rejected'
    PENDING = 'pending'
    STATUS = [
        (APPROVED, 'Request has been approved'),
        (REJECTED, 'Request has been rejected'),
        (PENDING, 'Request not yet evaluated')
    ]
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS, default=PENDING, max_length=8)
    request_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile} has requested {self.movie} at time {self.request_date}"

    class Meta:
        ordering = ["-request_date"]
        verbose_name_plural = 'Requests'
