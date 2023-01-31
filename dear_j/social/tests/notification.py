import pytest

from django import test
from rest_framework import status

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


@pytest.mark.django_db
def test_get_notification_networks(
    client: test.Client,
    user1: data_utils.UserData,
    user2: data_utils.UserData,
):
    """Test Get Notification Networks."""
    client.post(path="/api/v1/user/login/", data=user1.for_login, content_type="application/json")
    client.post(path="/api/v1/social/network/followee/", data={"followee": {"pk": 2}}, content_type="application/json")

    # Change User
    client.post(path="/api/v1/user/logout/")
    client.post(path="/api/v1/user/login/", data=user2.for_login, content_type="application/json")

    response = client.get(path="/api/v1/social/network/notification/")
    expected = [
        {
            "id": 1,
            "followee": {"pk": 2, "username": "user2", "email": "user2@example.com"},
            "approved": None,
            "follower": 1,
        },
    ]
    compare_utils.assert_response_equal(response, status.HTTP_200_OK, expected)

    client.patch(path="/api/v1/social/network/follower/1/", data={"approved": True}, content_type="application/json")
    response = client.get(path="/api/v1/social/network/notification/")
    compare_utils.assert_response_equal(response, status.HTTP_200_OK, [])
