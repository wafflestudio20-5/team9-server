from rest_framework import status
from rest_framework import test

from user import models


class LoginTestCase(test.APITestCase):
    def test_success_login(self):
        user = models.User.objects.create(email="testcase@example.com", birthday="2001-06-11")
        user.set_password("testcasePassword123")
        user.save()

        data = {"email": "testcase@example.com", "password": "testcasePassword123"}
        response = self.client.post("/api/v1/user/login/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fail_login(self):
        user = models.User.objects.create(email="testcase@example.com", birthday="2001-06-11")
        user.set_password("testcasePassword123")
        user.save()

        data = {"email": "testcase@example.com", "password": "testcase3"}
        response = self.client.post("/api/v1/user/login/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class RegisterTestCase(test.APITestCase):
    def test_success_register(self):
        data = {
            "username": "username123",
            "email": "email@naver.com",
            "password1": "testpassword*",
            "password2": "testpassword*",
            "birthday": "2022-12-27",
        }
        response = self.client.post("/api/v1/user/registration/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_fail_register(self):
        data = {
            "username": "username123",
            "email": "email@naver.com",
            "password1": "testpassword*",
            "password2": "testpasswo1d*",
            "birthday": "2022-12-27",
        }
        response = self.client.post("/api/v1/user/registration/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
