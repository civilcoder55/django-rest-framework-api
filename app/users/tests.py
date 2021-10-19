from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

import json

from rest_framework import status
from rest_framework.test import APIClient


CREATE_TOKEN_URL = reverse('users:token-create')
USER_DETAILS_URL = reverse('users:user-details')


def sample_user(username, password):
    """Create and return a sample user"""
    return get_user_model().objects.create_user(
        username=username, password=password
    )


class UsersApiTests(TestCase):
    """Test the users API"""

    def setUp(self):
        self.client = APIClient()

    def test_unauthenticated_user_cannot_access_profile(self):
        """Test user is required for profile API"""
        res = self.client.get(USER_DETAILS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_token_invalid_data(self):
        """Test user can't get token with invalid data"""

        payload = {'username': 'test_user', 'password': 'wrongpassword'}
        sample_user('test_user', 'correct_password')
        res = self.client.post(CREATE_TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual({'non_field_errors':
                          ['Unable to log in with provided credentials.']},
                         json.loads(res.content))

    def test_token_is_valid(self):
        """Test user can auth with generated token"""

        payload = {'username': 'test_user', 'password': 'correct_password'}
        sample_user('test_user', 'correct_password')
        res = self.client.post(CREATE_TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

        self.client = APIClient(
            HTTP_AUTHORIZATION='Token ' + res.data['token'])
        res = self.client.get(USER_DETAILS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['username'], payload['username'])
