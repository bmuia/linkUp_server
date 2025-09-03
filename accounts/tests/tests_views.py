from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

class UserServiceTests(APITestCase):

    def setUp(self):
        self.register_url = reverse('register-user')
        self.login_url = reverse('login-user')
        self.whoam_url = reverse('get-current-user')
        self.logout_url = reverse('logout-user')

        self.user_data = {
            'email': 'test@example.com',
            'username': 'test',
            'password': 'test'
        }

    def test_user_creation_view(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_login_view(self):
        self.client.post(self.register_url, self.user_data, format='json')
        response = self.client.post(self.login_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_current_user_view(self):
        self.client.post(self.register_url, self.user_data, format='json')
        token_response = self.client.post(self.login_url, self.user_data, format='json')
        access_token = token_response.data.get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.whoam_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_current_user_view(self):
        self.client.post(self.register_url, self.user_data, format='json')
        token_response = self.client.post(self.login_url, self.user_data, format='json')
        access_token = token_response.data.get('access')
        refresh_token = token_response.data.get('refresh')
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = self.client.post(self.logout_url, {"refresh": refresh_token}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

