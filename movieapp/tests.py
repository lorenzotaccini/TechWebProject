import json

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from .models import Movie, Request


class CreateRequestAjaxTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.movie = Movie.objects.create(tmdb_id=123, title='Test Movie', available=False)
        self.url = reverse('movieapp:create_request_ajax', kwargs={'pk': self.movie.pk})

    def test_create_request_as_anonymous_user(self):
        print('trying to make movie request as anonymous user, should be redirect to login page')
        self.client.logout()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)

    def test_create_request_success(self):
        print('trying to make a successful movie request')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['status'], 'success')

    def test_create_request_already_exists(self):
        print('trying to make an unsuccessful movie request because it is already existent for this movie and profile')
        Request.objects.create(profile=self.user.profile, movie=self.movie)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['status'], 'error')
        self.assertEqual(json.loads(response.content)['message'], 'Request already exists.')

    def test_create_request_movie_available(self):
        print('trying to make an unsuccessful movie request because movie is already available and there is no need to request it')
        self.movie.available = True
        self.movie.save()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['status'], 'error')

class RemoveRequestAjaxTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.movie = Movie.objects.create(tmdb_id=123, title='Test Movie', available=False)
        self.profile = self.user.profile
        self.request = Request.objects.create(profile=self.profile, movie=self.movie)
        self.url = reverse('movieapp:remove_request_ajax', kwargs={'pk': self.movie.pk})

    def test_remove_request_success(self):
        print('trying to succesfully remove a movie request from database')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['status'], 'success')

    def test_remove_request_not_exists(self):
        print('trying to unsuccessfully remove a movie request from database: request does not exist')
        self.request.delete()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['status'], 'error')

