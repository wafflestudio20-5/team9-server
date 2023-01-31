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
def test_create_recurring_schedules(
    client: test.Client,
    user1: data_utils.UserData,
    user2: data_utils.UserData,
    user3: data_utils.UserData,
):
    """Test create recurring schedules."""
    client.post(path="/api/v1/user/login/", data=user1.for_login, content_type="application/json")
    recurring_schedule_data = data_utils.ScheduleData.create_nth_schedule_data(
        n=1,
        protection_level=protection.ProtectionLevel.OPEN.value,
        participant_ids=[2, 3],
    ).as_dict()

    recurring_schedule_data.update(
        {
            "start_at": "2023-01-23 01:00:00",
            "end_at": "2023-01-23 01:30:00",
            "is_recurring": True,
            "cron_expr": "* * * * 1 *",
            "recurring_end_at": "2023-02-10 00:00:00",
        }
    )
    response = client.post(
        path="/api/v1/calendar/schedule/",
        data=recurring_schedule_data,
        content_type="application/json",
    )

    expected_parent_schedule = copy.deepcopy(recurring_schedule_data)
    expected_parent_schedule.update(
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
            "recurring_schedule_group": 1,
        }
    )
    expected_child_schedule_1 = copy.deepcopy(expected_parent_schedule)
    expected_child_schedule_2 = copy.deepcopy(expected_parent_schedule)
    expected_child_schedule_2.update(
        {
            "id": 2,
            "start_at": "2023-01-30 01:00:00",
            "end_at": "2023-01-30 01:30:00",
        }
    )
    expected_child_schedule_3 = copy.deepcopy(expected_parent_schedule)
    expected_child_schedule_3.update(
        {
            "id": 3,
            "start_at": "2023-02-06 01:00:00",
            "end_at": "2023-02-06 01:30:00",
        }
    )
    expected = [
        expected_child_schedule_1,
        expected_child_schedule_2,
        expected_child_schedule_3,
    ]

    compare_utils.assert_response_equal(response, status.HTTP_201_CREATED, expected)
    return expected


@pytest.mark.django_db
def test_update_and_destroy_recurring_schedules(
    client: test.Client,
    user1: data_utils.UserData,
    user2: data_utils.UserData,
    user3: data_utils.UserData,
):
    """Test update and destroy recurring schedules."""
    (
        child_schedule_1,
        child_schedule_2,
        child_schedule_3,
    ) = test_create_recurring_schedules(client, user1, user2, user3)

    new_data = {
        "start_at": "2023-02-06 02:00:00",
        "end_at": "2023-02-06 02:30:00",
        "participants": [{"pk": 2}],
    }

    response = client.patch(
        path="/api/v1/calendar/schedule/group/1/",
        data=new_data,
        content_type="application/json",
    )

    child_schedule_1.update(
        {
            "start_at": "2023-01-23 02:00:00",
            "end_at": "2023-01-23 02:30:00",
            "participants": [
                {
                    "pk": 2,
                    "username": "user2",
                    "email": "user2@example.com",
                },
            ],
        }
    )
    child_schedule_2.update(
        {
            "start_at": "2023-01-30 02:00:00",
            "end_at": "2023-01-30 02:30:00",
            "participants": [
                {
                    "pk": 2,
                    "username": "user2",
                    "email": "user2@example.com",
                },
            ],
        }
    )
    child_schedule_3.update(
        {
            "start_at": "2023-02-06 02:00:00",
            "end_at": "2023-02-06 02:30:00",
            "participants": [
                {
                    "pk": 2,
                    "username": "user2",
                    "email": "user2@example.com",
                },
            ],
        }
    )
    expected_recurring_schedule = [
        child_schedule_1,
        child_schedule_2,
        child_schedule_3,
    ]
    compare_utils.assert_json_equal(response.json()["schedules"], expected_recurring_schedule)

    response = client.delete(path="/api/v1/calendar/schedule/group/1/")
    compare_utils.assert_response_equal(response, status.HTTP_204_NO_CONTENT)

    target_uri = uri_utils.get_uri_with_extra_params(
        url="/api/v1/calendar/schedule/",
        extra_params={
            "pk": 1,
            "from": "2022-01-01",
            "to": "2023-03-01",
        },
    )
    response = client.get(target_uri)
    compare_utils.assert_response_equal(response, status.HTTP_200_OK, [])
