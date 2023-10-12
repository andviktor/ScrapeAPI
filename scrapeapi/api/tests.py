from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User, Project, Scraper, Element

class UserTests(APITestCase):

    def test_create_user(self):
        """
        Testing the creation of a new user object.
        """
        url = reverse('user-list')

        # Params: empty
        data = {}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Params: username
        data = {'username': 'testuser'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Params: username, password
        data = {
            'username': 'testuser',
            'password': 'testpass'
            }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Get token
        url_auth = reverse('auth')
        response = self.client.post(url_auth, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
