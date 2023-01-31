import copy

import pytest

from django import test
from rest_framework import status

from calendar_j.services.attendance import attendance
from calendar_j.services.protection import protection
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
def test_get_notification_schedules(
    client: test.Client,
    user1: data_utils.UserData,
    user2: data_utils.UserData,
):
    """Test Get Notification Schedules."""
    client.post(path="/api/v1/user/login/", data=user1.for_login, content_type="application/json")
    schedule_1_data = data_utils.ScheduleData.create_nth_schedule_data(
        n=1,
        protection_level=protection.ProtectionLevel.OPEN.value,
        participant_ids=[2],
    ).as_dict()
    schedule_2_data = data_utils.ScheduleData.create_nth_schedule_data(
        n=1,
        protection_level=protection.ProtectionLevel.OPEN.value,
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

    client.post(path="/api/v1/user/logout/")
    client.post(path="/api/v1/user/login/", data=user2.for_login, content_type="application/json")

    response = client.get(path="/api/v1/calendar/schedule/notification/")
    expected_schedule_1 = copy.deepcopy(schedule_1_data)
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
            ],
            "recurring_schedule_group": None,
        }
    )
    expected_schedule_2 = copy.deepcopy(schedule_2_data)
    expected_schedule_2.update(
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
    expected = [
        expected_schedule_1,
        expected_schedule_2,
    ]
    compare_utils.assert_response_equal(response, status.HTTP_200_OK, expected)

    client.patch(
        path="/api/v1/calendar/schedule/1/attendance/",
        data={"status": attendance.AttendanceStatus.HOLD},
        content_type="application/json",
    )
    response = client.get(path="/api/v1/calendar/schedule/notification/")
    expected = [expected_schedule_2]
    compare_utils.assert_response_equal(response, status.HTTP_200_OK, expected)

    client.patch(
        path="/api/v1/calendar/schedule/1/attendance/",
        data={"status": attendance.AttendanceStatus.ABSENCE},
        content_type="application/json",
    )
    response = client.get(path="/api/v1/calendar/schedule/notification/")
    expected = [expected_schedule_2]
    compare_utils.assert_response_equal(response, status.HTTP_200_OK, expected)

    client.patch(
        path="/api/v1/calendar/schedule/1/attendance/",
        data={"status": attendance.AttendanceStatus.PRESENCE},
        content_type="application/json",
    )
    response = client.get(path="/api/v1/calendar/schedule/notification/")
    expected = [expected_schedule_2]
    compare_utils.assert_response_equal(response, status.HTTP_200_OK, expected)
