import pytest

from django import test
from rest_framework import status

from utils.test import compare as compare_utils
from utils.test import data as data_utils

IMAGE_ADDRESS = "https://dear-j-blog.s3.ap-northeast-2.amazonaws.com/user/user.png"


@pytest.fixture(name="user1")
def fixture_registered_user1(client: test.Client):
    user1_data = data_utils.UserData.create_nth_user_data(1)
    client.post(path="/api/v1/user/registration/", data=user1_data.for_registration, content_type="application/json")
    return user1_data


@pytest.mark.django_db
def test_success_register(client: test.Client):
    user_data = data_utils.UserData.create_nth_user_data(1)
    response = client.post(path="/api/v1/user/registration/", data=user_data.for_registration, content_type="application/json")
    expected = {
        "user": {
            "pk": 1,
            "email": "user1@example.com",
            "birthdate": "2000-01-01",
            "username": "user1",
            "image": IMAGE_ADDRESS,
        }
    }
    compare_utils.assert_response_equal(response, status.HTTP_201_CREATED, expected, ("access_token", "refresh_token"))


@pytest.mark.django_db
def test_fail_register(client: test.Client):
    user_data = data_utils.UserData.create_nth_user_data(1)
    data = user_data.for_registration.copy()
    data["password2"] = "wrong_password"

    response = client.post(path="/api/v1/user/registration/", data=data, content_type="application/json")
    compare_utils.assert_response_equal(response, status.HTTP_400_BAD_REQUEST)


@pytest.mark.django_db
def test_success_login(client: test.Client, user1: data_utils.UserData):
    data = {"email": user1.email, "password": user1.password}
    response = client.post(path="/api/v1/user/login/", data=data, content_type="application/json")
    expected = {
        "user": {
            "pk": 1,
            "email": "user1@example.com",
            "birthdate": "2000-01-01",
            "username": "user1",
            "image": IMAGE_ADDRESS,
        }
    }
    compare_utils.assert_response_equal(response, status.HTTP_200_OK, expected, ("access_token", "refresh_token"))


@pytest.mark.django_db
def test_fail_login(client: test.Client, user1: data_utils.UserData):
    data = {"email": user1.email, "password": "wrong password"}
    response = client.post(path="/api/v1/user/login/", data=data, content_type="application/json")
    compare_utils.assert_response_equal(response, status.HTTP_400_BAD_REQUEST)


@pytest.mark.django_db
def test_success_change_pw(client: test.Client, user1: data_utils.UserData):
    data = {"email": user1.email, "password": user1.password}
    response = client.post(path="/api/v1/user/login/", data=data, content_type="application/json")
    data = {"new_password1": "user1password1*", "new_password2": "user1password1*", "old_password": user1.password}
    response = client.post(path="/api/v1/user/password/change/", data=data, content_type="application/json")
    expected = {"detail": "New password has been saved."}
    compare_utils.assert_response_equal(response, status.HTTP_200_OK, expected)


@pytest.mark.django_db
def test_update_profile(client: test.Client, user1: data_utils.UserData):
    data = {"email": user1.email, "password": user1.password}
    client.post(path="/api/v1/user/login/", data=data, content_type="application/json")

    update_data = {
        "birthdate": "2001-01-01",
    }
    response = client.patch(path="/api/v1/user/profile/", data=update_data, content_type="application/json")

    expected = {
        "pk": 1,
        "email": "user1@example.com",
        "birthdate": "2001-01-01",
        "username": "user1",
        "image": IMAGE_ADDRESS,
    }
    compare_utils.assert_response_equal(response, status.HTTP_200_OK, expected)


@pytest.mark.django_db
def test_refresh_token(client: test.Client, user1: data_utils.UserData):
    data = {"email": user1.email, "password": user1.password}
    response = client.post(path="/api/v1/user/login/", data=data, content_type="application/json")

    refresh = response.json().get("refresh_token")
    data = {"refresh": refresh}
    response = client.post(path="/api/v1/user/token/refresh/", data=data, content_type="application/json")

    actual = response.json()
    assert "access" in actual
    assert "access_token_expiration" in actual
    compare_utils.assert_response_equal(response, status.HTTP_200_OK)


@pytest.mark.django_db
def test_update_email(client: test.Client, user1: data_utils.UserData):
    data = {"email": user1.email, "password": user1.password}
    client.post(path="/api/v1/user/login/", data=data, content_type="application/json")

    update_data = {
        "email": "testuser@example.com",
    }
    response = client.patch(path="/api/v1/user/profile/", data=update_data, content_type="application/json")

    expected = {
        "pk": 1,
        "email": "testuser@example.com",
        "birthdate": "2001-01-01",
        "username": "user1",
        "image": IMAGE_ADDRESS,
    }
    compare_utils.assert_response_equal(response, status.HTTP_200_OK, expected)


@pytest.mark.django_db
def test_update_birthdate(client: test.Client, user1: data_utils.UserData):
    data = {"email": user1.email, "password": user1.password}
    client.post(path="/api/v1/user/login/", data=data, content_type="application/json")

    update_data = {
        "birthdate": "2000-01-01",
    }
    response = client.patch(path="/api/v1/user/profile/", data=update_data, content_type="application/json")

    expected = {
        "pk": 1,
        "email": "user1@example.com",
        "birthdate": "2000-01-01",
        "username": "user1",
        "image": IMAGE_ADDRESS,
    }
    compare_utils.assert_response_equal(response, status.HTTP_200_OK, expected)


@pytest.mark.django_db
def test_update_username(client: test.Client, user1: data_utils.UserData):
    data = {"email": user1.email, "password": user1.password}
    client.post(path="/api/v1/user/login/", data=data, content_type="application/json")

    update_data = {
        "username": "username",
    }
    response = client.patch(path="/api/v1/user/profile/", data=update_data, content_type="application/json")

    expected = {
        "pk": 1,
        "email": "user1@example.com",
        "birthdate": "2000-01-01",
        "username": "username",
        "image": IMAGE_ADDRESS,
    }
    compare_utils.assert_response_equal(response, status.HTTP_200_OK, expected)
