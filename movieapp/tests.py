import json
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from .models import Movie, Request, Profile

import requests

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


class MovieModelTest(TestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
            tmdb_id=1,
            title="Test Movie",
            year=2020,
            description="Test Description",
            genre=json.dumps(["Action", "Comedy"]),
            available=False
        )
        self.user = User.objects.create_user(username='testuser', password='pass')


    def test_get_genre_as_list(self):
        genre_list = self.movie.get_genre_as_list()
        self.assertEqual(genre_list, ["Action", "Comedy"])

    def test_are_requests_sync(self):
        # No requests, should be True
        self.assertTrue(self.movie.are_requests_sync())

        # Create requests with the same status
        request1 = Request.objects.create(profile=self.user.profile, movie=self.movie, status=Request.PENDING)
        other_user = User.objects.create_user(username='otheruser', password='pass')
        request2 = Request.objects.create(profile=other_user.profile, movie=self.movie, status=Request.PENDING)
        self.assertTrue(self.movie.are_requests_sync())

        # Create a request with a different status
        other_other_user = User.objects.create_user(username='otherotheruser', password='pass')
        request3 = Request.objects.create(profile=other_other_user.profile, movie=self.movie, status=Request.APPROVED)
        self.assertFalse(self.movie.are_requests_sync())

    def test_get_last_request(self):
        # No requests, should return None
        self.assertIsNone(self.movie.get_last_request())

        # Create requests
        request1 = Request.objects.create(profile=self.user.profile, movie=self.movie)

        other_user = User.objects.create_user(username='otheruser', password='pass')
        request2 = Request.objects.create(profile=other_user.profile, movie=self.movie, request_date=request1.request_date + timezone.timedelta(days=1))

        # The last request should be request2
        self.assertEqual(self.movie.get_last_request(), request2)

    @patch('requests.get')
    def test_poster_url(self, mock_get):
        # Mock the response from the TMDB API
        mock_response = {
            'poster_path': '/testposter.jpg'
        }
        mock_get.return_value.json.return_value = mock_response

        expected_url = 'https://image.tmdb.org/t/p/w342/testposter.jpg'
        self.assertEqual(self.movie.poster_url, expected_url)

        # Test case where there is no poster path
        mock_response = {}
        mock_get.return_value.json.return_value = mock_response
        self.assertIsNone(self.movie.poster_url)

        # Test case where the API request fails
        mock_get.side_effect = requests.exceptions.RequestException
        self.assertIsNone(self.movie.poster_url)
