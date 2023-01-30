import pytest

from django import test
from rest_framework import status

from utils.test import data as data_utils


@pytest.fixture(name="user1")
def fixture_registered_user1(client: test.Client):
    user1_data = data_utils.UserData.create_nth_user_data(1)
    client.post(path="/api/v1/user/registration/", data=user1_data.for_registration, content_type="application/json")
    return user1_data


@pytest.fixture(name="user2")
def fixture_registered_user2(client: test.Client):
    user2_data = data_utils.UserData.create_nth_user_data(2)
    client.post(path="/api/v1/user/registration/", data=user2_data.for_registration, content_type="application/json")
    return user2_data


@pytest.fixture(name="user3")
def fixture_registered_user3(client: test.Client):
    user3_data = data_utils.UserData.create_nth_user_data(3)
    client.post(path="/api/v1/user/registration/", data=user3_data.for_registration, content_type="application/json")
    return user3_data


@pytest.fixture(name="user4")
def fixture_registered_user4(client: test.Client):
    user4_data = data_utils.UserData.create_nth_user_data(4)
    client.post(path="/api/v1/user/registration/", data=user4_data.for_registration, content_type="application/json")
    return user4_data


@pytest.mark.django_db
def test_search_candidate(
    client: test.Client,
    user1: data_utils.UserData,
    user2: data_utils.UserData,
    user3: data_utils.UserData,
    user4: data_utils.UserData,
):
    """Test Search Candidate to follow API."""
    response = client.get(path="/api/v1/social/search/candidate/?search=user")
    expected = [
        {
            "pk": 1,
            "username": "user1",
            "email": "user1@example.com",
        },
        {
            "pk": 2,
            "username": "user2",
            "email": "user2@example.com",
        },
        {
            "pk": 3,
            "username": "user3",
            "email": "user3@example.com",
        },
        {
            "pk": 4,
            "username": "user4",
            "email": "user4@example.com",
        },
    ]
    actual = response.json()["results"]

    assert response.status_code == status.HTTP_200_OK
    for actual_row, expected_row in zip(actual, expected):
        for key, value in expected_row.items():
            assert key in actual_row.keys()
            assert actual_row[key] == value

    response = client.get(path="/api/v1/social/search/candidate/?search=user3")
    expected = [
        {
            "pk": 3,
            "username": "user3",
            "email": "user3@example.com",
        },
    ]
    actual = response.json()["results"]

    assert response.status_code == status.HTTP_200_OK
    for actual_row, expected_row in zip(actual, expected):
        for key, value in expected_row.items():
            assert key in actual_row.keys()
            assert actual_row[key] == value
