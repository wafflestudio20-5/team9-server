from django.test import TestCase
from django import urls

from rest_framework import test
from rest_framework import status


# Create your tests here.


class RegisterTestCase(test.APITestCase):
    def test_register(self):
        data = {
            "email": "testcase@example.com",
            "password1": "NewPassword@123",
            "password2": "NewPassword@123"
        }
        response = self.client.post(urls.reverse(
            'user:registration'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
