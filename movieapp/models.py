from os.path import join

from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Movie(models.Model):
    tmdb_id = models.IntegerField(primary_key=True)  # useful to retrieve data from TMDB APIs
    title = models.CharField(max_length=100)
    year = models.DateField()
    description = models.TextField(max_length=1000)
    genre = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title} - {self.tmdb_id}"

    class Meta:
        ordering = ["-pk"]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    propic = models.ImageField(
        upload_to='users_pics',
        default=join('static', 'unknown_user.png'),
        blank=True
    )
    requests = models.ManyToManyField(Movie, through='Request', blank=True, related_name='requests')
    watchlisted = models.ManyToManyField(Movie, blank=True, related_name='watchlisted')

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
