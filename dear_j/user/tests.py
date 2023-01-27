import pytest

from django import test
from rest_framework import status

from utils.test import compare
from utils.test import data as data_utils

@pytest.fixture(name="user1")
def fixture_registered_user1(client: test.Client):
    user1_data = data_utils.UserData.create_nth_user_data(1)
    client.post(path="/api/v1/user/registration/", data=user1_data.for_registration, content_type="application/json")
    return user1_data


@pytest.mark.django_db
def test_success_register(client: test.Client):
    user_data = data_utils.UserData.create_nth_user_data(1)
    response = client.post(path="/api/v1/user/registration/", data=user_data.for_registration, content_type="application/json")
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_fail_register(client: test.Client):
    user_data = data_utils.UserData.create_nth_user_data(1)
    data = user_data.for_registration.copy()
    data["password2"] = "wrong_password"

    response = client.post(path="/api/v1/user/registration/", data=data, content_type="application/json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_success_login(client: test.Client, user1: data_utils.UserData):
    data = {"email": user1.email, "password": user1.password}
    response = client.post(path="/api/v1/user/login/", data=data, content_type="application/json")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_fail_login(client: test.Client, user1: data_utils.UserData):
    data = {"email": user1.email, "password": "wrong password"}
    response = client.post(path="/api/v1/user/login/", data=data, content_type="application/json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_success_change_pw(client: test.Client, user1: data_utils.UserData):
    data = {"email": user1.email, "password": user1.password}
    response = client.post(path="/api/v1/user/login/", data=data, content_type="application/json")
    data = {"new_password1": "user1password1*", "new_password2": "user1password1*",
            "old_password":user1.password}
    response = client.post(path="/api/v1/user/password/change/", data=data, content_type="application/json")
    actual = response.json()
    expected = {"detail":"New password has been saved."}
    compare.assert_json_equal(actual, expected)
    assert response.status_code == status.HTTP_200_OK
