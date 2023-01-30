import copy

import pytest

from django import test
from rest_framework import status

from calendar_j.services.protection import protection
from utils import uri as uri_utils
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


@pytest.mark.django_db
def test_create_normal_schedule(
    client: test.Client,
    user1: data_utils.UserData,
    user2: data_utils.UserData,
    user3: data_utils.UserData,
):
    """Test create normal schedule."""
    client.post(path="/api/v1/user/login/", data=user1.for_login, content_type="application/json")
    schedule_data = data_utils.ScheduleData.create_nth_schedule_data(
        n=1,
        protection_level=protection.ProtectionLevel.OPEN.value,
        participant_ids=[2, 3],
    ).as_dict()

    response = client.post(
        path="/api/v1/calendar/schedule/",
        data=schedule_data,
        content_type="application/json",
    )
    expected = copy.deepcopy(schedule_data)
    expected.update(
        {
            "id": 1,
            "created_by": 1,
            "participants": [
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
            ],
            "recurring_schedule_group": None,
        }
    )

    compare_utils.assert_response_equal(response, status.HTTP_201_CREATED, expected)


@pytest.mark.django_db
def test_get_schedules_filtered_by_period(
    client: test.Client,
    user1: data_utils.UserData,
    user2: data_utils.UserData,
    user3: data_utils.UserData,
):
    """Test get wanted schedule : Period Condition."""
    client.post(path="/api/v1/user/login/", data=user1.for_login, content_type="application/json")

    schedule_1_data = data_utils.ScheduleData.create_nth_schedule_data(
        n=1,
        protection_level=protection.ProtectionLevel.OPEN.value,
        participant_ids=[2, 3],
    ).as_dict()

    schedule_2_data = data_utils.ScheduleData.create_nth_schedule_data(
        n=2,
        protection_level=protection.ProtectionLevel.OPEN.value,
        participant_ids=[2],
    ).as_dict()
    schedule_3_data = data_utils.ScheduleData.create_nth_schedule_data(
        n=2,
        protection_level=protection.ProtectionLevel.OPEN.value,
        participant_ids=[3],
    ).as_dict()

    schedule_1_data.update(
        {
            "start_at": "2022-12-11 00:00:00",
            "end_at": "2022-12-12 00:00:00",
        }
    )
    schedule_2_data.update(
        {
            "start_at": "2022-12-13 00:00:00",
            "end_at": "2022-12-14 00:00:00",
        }
    )
    schedule_3_data.update(
        {
            "start_at": "2022-12-15 00:00:00",
            "end_at": "2022-12-16 00:00:00",
        }
    )

    client.post(
        path="/api/v1/calendar/schedule/",
        data=schedule_1_data,
        content_type="application/json",
    )
    client.post(
        path="/api/v1/calendar/schedule/",
        data=schedule_2_data,
        content_type="application/json",
    )
    client.post(
        path="/api/v1/calendar/schedule/",
        data=schedule_3_data,
        content_type="application/json",
    )

    response = client.get(
        uri_utils.get_uri_with_extra_params(
            url="/api/v1/calendar/schedule/",
            extra_params={
                "pk": 1,
                "from": "2022-12-13",
                "to": "2022-12-14",
            },
        )
    )

    expected_schedule = copy.deepcopy(schedule_2_data)
    expected_schedule.update(
        {
            "id": 2,
            "created_by": 1,
            "participants": [
                {
                    "pk": 2,
                    "username": "user2",
                    "email": "user2@example.com",
                },
            ],
            "recurring_schedule_group": None,
        }
    )

    expected = [expected_schedule]
    compare_utils.assert_response_equal(response, status.HTTP_200_OK, expected)


@pytest.mark.django_db
def test_get_authorized_schedules(
    client: test.Client,
    user1: data_utils.UserData,
    user2: data_utils.UserData,
    user3: data_utils.UserData,
):
    """Test get wanted schedule : Permission Level & Social Network Condition."""
    client.post(path="/api/v1/user/login/", data=user1.for_login, content_type="application/json")

    schedule_1_data = data_utils.ScheduleData.create_nth_schedule_data(
        n=1,
        protection_level=protection.ProtectionLevel.OPEN.value,
        participant_ids=[2, 3],
    ).as_dict()
    schedule_2_data = data_utils.ScheduleData.create_nth_schedule_data(
        n=2,
        protection_level=protection.ProtectionLevel.FOLLOWER.value,
        participant_ids=[3],
    ).as_dict()
    schedule_3_data = data_utils.ScheduleData.create_nth_schedule_data(
        n=2,
        protection_level=protection.ProtectionLevel.CLOSED.value,
        participant_ids=[2],
    ).as_dict()

    client.post(
        path="/api/v1/calendar/schedule/",
        data=schedule_1_data,
        content_type="application/json",
    )
    client.post(
        path="/api/v1/calendar/schedule/",
        data=schedule_2_data,
        content_type="application/json",
    )
    client.post(
        path="/api/v1/calendar/schedule/",
        data=schedule_3_data,
        content_type="application/json",
    )

    response = client.get(
        uri_utils.get_uri_with_extra_params(
            url="/api/v1/calendar/schedule/",
            extra_params={
                "pk": 1,
                "from": "2022-12-11",
                "to": "2022-12-12",
            },
        )
    )

    expected_schedule_1 = copy.deepcopy(schedule_1_data)
    expected_schedule_2 = copy.deepcopy(schedule_2_data)
    expected_schedule_3 = copy.deepcopy(schedule_3_data)

    expected_schedule_1.update(
        {
            "id": 1,
            "created_by": 1,
            "participants": [
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
            ],
            "recurring_schedule_group": None,
        }
    )
    expected_schedule_2.update(
        {
            "id": 2,
            "created_by": 1,
            "participants": [
                {
                    "pk": 3,
                    "username": "user3",
                    "email": "user3@example.com",
                },
            ],
            "recurring_schedule_group": None,
        }
    )
    expected_schedule_3.update(
        {
            "id": 3,
            "created_by": 1,
            "participants": [
                {
                    "pk": 2,
                    "username": "user2",
                    "email": "user2@example.com",
                },
            ],
            "recurring_schedule_group": None,
        }
    )
    expected = [
        expected_schedule_1,
        expected_schedule_2,
        expected_schedule_3,
    ]
    compare_utils.assert_response_equal(response, status.HTTP_200_OK, expected)

    response = client.get(
        uri_utils.get_uri_with_extra_params(
            url="/api/v1/calendar/schedule/",
            extra_params={
                "pk": 2,
                "from": "2022-12-11",
                "to": "2022-12-12",
            },
        )
    )

    compare_utils.assert_response_equal(response, status.HTTP_200_OK, [])

    # (User 1)Request to want follow
    response = client.post(path="/api/v1/social/network/followee/", data={"followee": {"pk": 2}}, content_type="application/json")
    client.post(path="/api/v1/user/logout/")

    # (User 2) Accept follow
    client.post(path="/api/v1/user/login/", data=user2.for_login, content_type="application/json")
    response = client.patch(path="/api/v1/social/network/follower/1/", data={"approved": True}, content_type="application/json")
    client.post(path="/api/v1/user/logout/")

    # (User 1) Come back
    client.post(path="/api/v1/user/login/", data=user1.for_login, content_type="application/json")

    response = client.get(
        uri_utils.get_uri_with_extra_params(
            url="/api/v1/calendar/schedule/",
            extra_params={
                "pk": 2,
                "from": "2022-12-11",
                "to": "2022-12-12",
            },
        )
    )
    expected = [expected_schedule_1]
    compare_utils.assert_response_equal(response, status.HTTP_200_OK, expected)


@pytest.mark.django_db
def test_update_and_delete_schedule(
    client: test.Client,
    user1: data_utils.UserData,
    user2: data_utils.UserData,
    user3: data_utils.UserData,
):
    """Test Schedule (Partial or Total) Update & Delete API."""
    client.post("/api/v1/user/login/", data=user1.for_login, content_type="application/json")

    schedule_data = data_utils.ScheduleData.create_nth_schedule_data(
        n=1,
        protection_level=protection.ProtectionLevel.OPEN.value,
        participant_ids=[],
    ).as_dict()
    client.post(
        path="/api/v1/calendar/schedule/",
        data=schedule_data,
        content_type="application/json",
    )

    # Check Patch (Partial Update)
    response = client.patch(
        path="/api/v1/calendar/schedule/1/",
        data={
            "participants": [{"pk": 2}],
            "title": "Modified Test Schedule 1-1",
        },
        content_type="application/json",
    )
    expected = copy.deepcopy(schedule_data)
    expected.update(
        {
            "id": 1,
            "title": "Modified Test Schedule 1-1",
            "created_by": 1,
            "participants": [
                {
                    "pk": 2,
                    "username": "user2",
                    "email": "user2@example.com",
                },
            ],
            "recurring_schedule_group": None,
        }
    )
    compare_utils.assert_response_equal(response, status.HTTP_200_OK, expected)

    # Check Put (Total Update)
    modified_schedule_data = copy.deepcopy(schedule_data)
    # Total Update
    modified_schedule_data.update(
        {
            "title": "Second Modified Test Schedule 1-1",
            "start_at": "2022-12-12 00:00:00",
            "end_at": "2022-12-13 00:00:00",
            "description": "Second Modified Test description 1-1",
        }
    )
    response = client.put(
        path="/api/v1/calendar/schedule/1/",
        data=modified_schedule_data,
        content_type="application/json",
    )
    expected = copy.deepcopy(modified_schedule_data)
    expected.update(
        {
            "id": 1,
            "title": "Second Modified Test Schedule 1-1",
            "start_at": "2022-12-12 00:00:00",
            "end_at": "2022-12-13 00:00:00",
            "description": "Second Modified Test description 1-1",
            "created_by": 1,
            "participants": [],
            "recurring_schedule_group": None,
        }
    )
    compare_utils.assert_response_equal(response, status.HTTP_200_OK, expected)

    # Check Delete
    response = client.delete(path="/api/v1/calendar/schedule/1/", content_type="application/json")
    compare_utils.assert_response_equal(response, status.HTTP_204_NO_CONTENT)

    response = client.get(path="/api/v1/calendar/schedule/1/", content_type="application/json")
    compare_utils.assert_response_equal(response, status.HTTP_404_NOT_FOUND)
