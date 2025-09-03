from rest_framework.test import APITestCase
from accounts.serializers import RegistrationSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class RegistrationSerializerTest(APITestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'username': 'test',
            'password': 'test'
        }

    def test_user_creation_serializer(self):
        serializer = RegistrationSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.username, self.user_data['username'])
        self.assertTrue(user.check_password(self.user_data['password']))
