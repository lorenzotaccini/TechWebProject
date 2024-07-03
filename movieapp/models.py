import json
from os.path import join

import requests
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


# Create your models here.

class Movie(models.Model):
    tmdb_id = models.IntegerField(primary_key=True)  # useful to retrieve data from TMDB APIs
    title = models.CharField(max_length=100)
    year = models.IntegerField(null=True)
    description = models.TextField(max_length=1000)
    genre = models.CharField(max_length=100)
    available = models.BooleanField(default=False)

    def get_genre_as_list(self):
        return json.loads(self.genre)

    def are_requests_sync(self):
        # Get all requests for this movie
        requests = self.movie_requests.all()

        if not requests.exists():
            return True

        # Get the status of the first request
        first_status = requests.first().status

        # Check if all other requests have the same status
        return all(req.status == first_status for req in requests)


    @property
    def poster_url(self):
        api_key = '5dbf33ab1210565bba9d880c176bf3d8'
        base_url = f'https://api.themoviedb.org/3/movie/{self.tmdb_id}?api_key={api_key}'


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


    def __str__(self):
        return f"{self.title} - {self.tmdb_id}"

    class Meta:
        ordering = ["-pk"]
        verbose_name_plural = 'Movies'


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    propic = models.ImageField(
        upload_to='users_pics',
        default=join('static', 'unknown_user.png'),
        blank=True
    )
    requests = models.ManyToManyField(Movie, through='Request', blank=True, related_name='requested_by', default=None)
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
    profile = models.ForeignKey(Profile, related_name='profile', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='movie_requests', on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS, default=PENDING, max_length=8)
    request_date = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.movie.available:
            raise ValidationError('Cannot request a movie that is already available.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.profile} requested {self.movie} at time {self.request_date}, status {self.status}"

    class Meta:
        ordering = ["-request_date"]
        verbose_name_plural = 'Requests'
        constraints = [
            models.UniqueConstraint(fields=['profile', 'movie'], name='unique_profile_movie_request')
        ]
