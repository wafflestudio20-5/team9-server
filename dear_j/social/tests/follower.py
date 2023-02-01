import pytest

from django import test
from rest_framework import status

from social.tests import followee as followee_tests
from utils.test import compare as compare_utils
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
def test_follower_list_network(
    client: test.Client,
    user1: data_utils.UserData,
    user2: data_utils.UserData,
):
    """Test Get List of Follow Requests API."""
    followee_tests.test_followee_list_and_create_network(client, user1, user2)
    client.post(path="/api/v1/user/logout/")
    client.post(path="/api/v1/user/login/", data=user2.for_login, content_type="application/json")
    response = client.get(path="/api/v1/social/network/follower/")
    expected = [
        {
            "id": 1,
            "followee": {
                "pk": 2,
                "username": "user2",
                "email": "user2@example.com",
            },
            "approved": None,
            "follower": 1,
        }
    ]
    compare_utils.assert_response_equal(response, status.HTTP_200_OK, expected)


@pytest.mark.django_db
def test_follower_update_network(
    client: test.Client,
    user1: data_utils.UserData,
    user2: data_utils.UserData,
):
    """Test Response for Follow Requests API."""
    test_follower_list_network(client, user1, user2)
    response = client.patch(path="/api/v1/social/network/follower/1/", data={"approved": True}, content_type="application/json")
    expected = {
        "id": 1,
        "followee": {
            "pk": 2,
            "username": "user2",
            "email": "user2@example.com",
        },
        "approved": True,
        "follower": 1,
    }
    compare_utils.assert_response_equal(response, status.HTTP_200_OK, expected)
