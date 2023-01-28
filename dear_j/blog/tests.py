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


@pytest.mark.django_db
def test_create_post(
    client: test.Client,
    user1: data_utils.UserData,
    user2: data_utils.UserData,
):
    client.post(path="/api/v1/user/login/", data=user1.for_login, content_type="application/json")

    post_data = {
        "title":"title",
        "content":"content"
    }
    response = client.post(
        path="/api/v1/blog/post/",
        data=post_data
    )
    expected = {
        "pid": 1,
        "title": "title",
        "content": "content",
        "created_by": 1
    }
    actual = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    for key, value in expected.items():
        assert key in actual.keys()
        assert actual[key] == value


@pytest.mark.django_db
def test_get_post(
    client: test.Client,
    user1: data_utils.UserData,
    user2: data_utils.UserData,
):
    client.post(path="/api/v1/user/login/", data=user1.for_login, content_type="application/json")

    post_data = {"title":"title", "content":"content"}
    response = client.post(
        path="/api/v1/blog/post/",
        data=post_data,
        content_type="application/json",
    )
    expected = {
        "pid": 1,
        "title": "title",
        "content": "content",
        "created_by": 1
    }
    actual = response.json()
    for key, value in expected.items():
        assert key in actual.keys()
        assert actual[key] == value

    assert response.status_code == status.HTTP_201_CREATED

    response = client.get("/api/v1/blog/post/1/")

    expected = {
        "pid": 1,
        "title": "title",
        "content": "content",
        "created_by": 1
    }
    assert response.status_code == status.HTTP_200_OK
    for key, value in expected.items():
        assert key in actual.keys()
        assert actual[key] == value


@pytest.mark.django_db
def test_create_comment(
    client: test.Client,
    user1: data_utils.UserData,
    user2: data_utils.UserData,
):
    client.post(path="/api/v1/user/login/", data=user1.for_login, content_type="application/json")

    post_data = {"title":"title", "content":"content"}
    response = client.post(
        path="/api/v1/blog/post/",
        data=post_data,
        content_type="application/json",
    )
    expected = {
        "pid": 1,
        "title": "title",
        "content": "content",
        "created_by": 1
    }
    actual = response.json()
    for key, value in expected.items():
        assert key in actual.keys()
        assert actual[key] == value
    assert response.status_code == status.HTTP_201_CREATED

    client.post("/api/v1/user/logout/")
    client.post("/api/v1/user/login/", data=user2.for_login, content_type="application/json")

    comment_data = {"post":1, "content":"content"}
    response = client.post(
        path="/api/v1/blog/comment/",
        data=comment_data,
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_201_CREATED
    actual = response.json()
    expected = {"cid": 1, "content": "content", "created_by": 2}

    for key, value in expected.items():
        assert key in actual.keys()
        assert actual[key] == value


@pytest.mark.django_db
def test_update_comment(
    client: test.Client,
    user1: data_utils.UserData,
    user2: data_utils.UserData,
):
    client.post(path="/api/v1/user/login/", data=user1.for_login, content_type="application/json")

    post_data = {"title":"title", "content":"content"}
    response = client.post(
        path="/api/v1/blog/post/",
        data=post_data,
        content_type="application/json",
    )
    expected = {
        "pid": 1,
        "title": "title",
        "content": "content",
        "created_by": 1
    }
    actual = response.json()
    for key, value in expected.items():
        assert key in actual.keys()
        assert actual[key] == value
    assert response.status_code == status.HTTP_201_CREATED

    client.post("/api/v1/user/logout/")
    client.post("/api/v1/user/login/", data=user2.for_login, content_type="application/json")

    comment_data = {"post":1, "content":"content"}
    response = client.post(
        path="/api/v1/blog/comment/",
        data=comment_data,
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_201_CREATED
    actual = response.json()
    expected = {"cid": 1, "content": "content", "created_by": 2}

    for key, value in expected.items():
        assert key in actual.keys()
        assert actual[key] == value

    response = client.get("/api/v1/blog/comment/1/")
    assert response.status_code == status.HTTP_200_OK


    response = client.patch(
        path="/api/v1/blog/comment/1/",
        data={"content": "modified"},
        content_type="application/json",
    )
    actual = response.json()

    expected = {
        "cid": 1,
        "content": "modified",
        "created_by": 2,
        "is_updated": True
    }

    for key, value in expected.items():
        assert key in actual.keys()
        assert actual[key] == value
