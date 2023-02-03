import pytest

from django import test
from rest_framework import status

from utils.test import compare as compare_utils
from utils.test import data as data_utils


@pytest.fixture(name="user1")
def fixture_registered_user1(client: test.Client):
    """Create registered user"""
    user1_data = data_utils.UserData.create_nth_user_data(1)
    client.post(path="/api/v1/user/registration/", data=user1_data.for_registration, content_type="application/json")
    return user1_data


@pytest.fixture(name="user2")
def fixture_registered_user2(client: test.Client):
    """Create registered user"""
    user2_data = data_utils.UserData.create_nth_user_data(2)
    client.post(path="/api/v1/user/registration/", data=user2_data.for_registration, content_type="application/json")
    return user2_data


@pytest.mark.django_db
def test_create_comment(
    client: test.Client,
    user1: data_utils.UserData,
    user2: data_utils.UserData,
):
    """Create Comment to Post"""
    client.post(path="/api/v1/user/login/", data=user1.for_login, content_type="application/json")

    post_data = {"title": "Test Title", "content": "Test Content"}
    response = client.post(
        path="/api/v1/blog/post/",
        data=post_data,
        content_type="application/json",
    )
    post_data = data_utils.PostData.create_post_data(schedules_list=[1, 2])

    expected = {
        "pid": 1,
        "title": "Test Title",
        "content": "Test Content",
        "created_by": 1,
        "schedules": [],
    }
    compare_utils.assert_response_equal(response, status.HTTP_201_CREATED, expected, ["created_at", "updated_at", "image"])

    client.post("/api/v1/user/logout/")
    client.post("/api/v1/user/login/", data=user2.for_login, content_type="application/json")

    comment_data = {"post": 1, "content": "Test Content"}
    response = client.post(
        path="/api/v1/blog/post/1/comment/",
        data=comment_data,
        content_type="application/json",
    )
    expected = {"post": 1, "cid": 1, "content": "Test Content", "created_by": 2, "is_updated": False}
    compare_utils.assert_response_equal(response, status.HTTP_201_CREATED, expected, ["created_at", "updated_at"])


@pytest.mark.django_db
def test_update_comment(
    client: test.Client,
    user1: data_utils.UserData,
    user2: data_utils.UserData,
):
    """Update Comment and check is_updated = True"""
    client.post(path="/api/v1/user/login/", data=user1.for_login, content_type="application/json")

    post_data = {"title": "Test Title", "content": "Test Content"}
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
        "schedules": [],
    }
    compare_utils.assert_response_equal(response, status.HTTP_201_CREATED, expected, ["created_at", "updated_at", "image"])

    client.post(path="/api/v1/user/logout/")
    client.post(path="/api/v1/user/login/", data=user2.for_login, content_type="application/json")

    comment_data = {"content": "Test Content"}
    response = client.post(
        path="/api/v1/blog/post/1/comment/",
        data=comment_data,
        content_type="application/json",
    )
    expected = {"post": 1, "cid": 1, "content": "Test Content", "created_by": 2, "is_updated": False}
    compare_utils.assert_response_equal(response, status.HTTP_201_CREATED, expected, ["created_at", "updated_at"])

    response = client.get(path="/api/v1/blog/comment/1/")
    compare_utils.assert_response_equal(response, status.HTTP_200_OK)

    response = client.patch(
        path="/api/v1/blog/comment/1/",
        data={"content": "Test Patch"},
        content_type="application/json",
    )
    expected = {"post": 1, "cid": 1, "content": "Test Patch", "created_by": 2, "is_updated": True}
    compare_utils.assert_response_equal(response, status.HTTP_200_OK, expected, ["created_at", "updated_at"])
