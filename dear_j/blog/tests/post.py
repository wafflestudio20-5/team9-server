import json

import pytest

from django import test
from rest_framework import status

from utils.test import compare as compare_utils
from utils.test import data as data_utils


@pytest.fixture(name="user3")
def fixture_registered_user1(client: test.Client):
    """Create registered user"""
    user1_data = data_utils.UserData.create_nth_user_data(1)
    client.post(path="/api/v1/user/registration/", data=user1_data.for_registration, content_type="application/json")
    return user1_data


@pytest.fixture(name="user4")
def fixture_registered_user2(client: test.Client):
    """Create registered user"""
    user2_data = data_utils.UserData.create_nth_user_data(2)
    client.post(path="/api/v1/user/registration/", data=user2_data.for_registration, content_type="application/json")
    return user2_data


@pytest.mark.django_db
def test_create_post(
    client: test.Client,
    user3: data_utils.UserData,
    user4: data_utils.UserData,
):
    """Create Post"""
    client.post(path="/api/v1/user/login/", data=user3.for_login, content_type="application/json")

    schedule_data_1 = data_utils.ScheduleData.create_nth_schedule_data(1, 1, [2, 3]).as_dict()

    response = client.post(
        path="/api/v1/calendar/schedule/",
        data=schedule_data_1,
        content_type="application/json",
    )
    schedule_data_2 = data_utils.ScheduleData.create_nth_schedule_data(1, 1, [2, 3]).as_dict()

    response = client.post(
        path="/api/v1/calendar/schedule/",
        data=schedule_data_2,
        content_type="application/json",
    )

    post_data = {"title": "Test Title", "content": "Test Content"}
    post_data["schedules_json"] = [{"pk": 1}, {"pk": 2}]
    response = client.post(
        path="/api/v1/blog/post/",
        data=post_data,
        content_type="application/json",
    )
    expected = {
        "pid": 1,
        "title": "Test Title",
        "content": "Test Content",
        "created_by": 1,
    }
    compare_utils.assert_response_equal(response, status.HTTP_201_CREATED, expected, ["created_at", "updated_at", "image", "schedules"])


@pytest.mark.django_db
def test_get_post(
    client: test.Client,
    user3: data_utils.UserData,
    user4: data_utils.UserData,
):
    """Get post that is connected with Schedules"""
    client.post(path="/api/v1/user/login/", data=user3.for_login, content_type="application/json")
    schedule_data_1 = data_utils.ScheduleData.create_nth_schedule_data(1, 1, [2, 3]).as_dict()
    response = client.post(path="/api/v1/calendar/schedule/", data=schedule_data_1, content_type="application/json")
    schedule_data_2 = data_utils.ScheduleData.create_nth_schedule_data(1, 1, [2, 3]).as_dict()
    response = client.post(path="/api/v1/calendar/schedule/", data=schedule_data_2, content_type="application/json")

    post_data = {"title": "Test Title", "content": "Test Content"}
    post_data["schedules_json"] = [{"pk": 1}, {"pk": 2}]
    response = client.post(
        path="/api/v1/blog/post/",
        data=post_data,
        content_type="application/json",
    )
    compare_utils.assert_response_equal(response, status.HTTP_201_CREATED)

    response = client.get(path="/api/v1/blog/post/1/")
    expected = {
        "pid": 1,
        "title": "Test Title",
        "content": "Test Content",
        "created_by": 1,
    }
    compare_utils.assert_response_equal(response, status.HTTP_200_OK, expected, ["created_at", "updated_at", "image", "schedules"])


@pytest.mark.django_db
def test_update_post(
    client: test.Client,
    user3: data_utils.UserData,
    user4: data_utils.UserData,
):
    test_create_post(client, user3, user4)
    updated_post_data = {
        "title": "Test Title : Modified",
    }
    response = client.patch(
        path="/api/v1/blog/post/1/",
        data=updated_post_data,
        content_type="application/json",
    )
    expected = {
        "pid": 1,
        "title": "Test Title : Modified",
        "content": "Test Content",
        "created_by": 1,
    }
    compare_utils.assert_response_equal(response, status.HTTP_200_OK, expected, ["created_at", "updated_at", "image", "schedules"])
