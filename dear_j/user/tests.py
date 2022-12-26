from rest_framework import status
from rest_framework import test

from user import models


class RegisterTestCase(test.APITestCase):
    def test_success_register(self):
        data = {"email": "testcase@example.com", "password1": "NewPassword@123", "password2": "NewPassword@123"}
        response = self.client.post("/api/v1/user/registration/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_fail_register(self):
        data = {"email": "testcase@example.com", "password1": "NewPassword@123", "password2": "NewPassword@122"}
        response = self.client.post("/api/v1/user/registration/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTestCase(test.APITestCase):
    def test_success_login(self):
        user = models.User.objects.create(email="testcase@example.com")
        user.set_password("testcasePassword123")
        user.save()

        data = {"email": "testcase@example.com", "password": "testcasePassword123"}
        response = self.client.post("/api/v1/user/login/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fail_login(self):
        user = models.User.objects.create(email="testcase@example.com")
        user.set_password("testcasePassword123")
        user.save()

        data = {"email": "testcase@example.com", "password": "testcase3"}
        response = self.client.post("/api/v1/user/login/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
