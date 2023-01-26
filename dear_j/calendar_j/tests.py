import copy
import dataclasses

import pytest

from django import test
from rest_framework import status

from calendar_j import models as calendar_models
from calendar_j import serializers as calendar_serializers
from calendar_j.services.protection import protection
from utils import uri as uri_utils
from utils.test import compare as compare_utils
from utils.test import data as data_utils

_EXCEPTION_COLUMNS = ("created_at", "updated_at")


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
def test_create_schedule(
    client: test.Client,
    user1: data_utils.UserData,
    user2: data_utils.UserData,
    user3: data_utils.UserData,
):
    client.post(path="/api/v1/user/login/", data=user1.for_login, content_type="application/json")
    schedule_data = data_utils.ScheduleData.create_nth_schedule_data(1, 1, [2, 3]).as_dict()

    response = client.post(
        path="/api/v1/calendar/schedule/",
        data=schedule_data,
        content_type="application/json",
    )
    expected = {
        "id": 1,
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
        "title": "Test Schedule 1",
        "protection_level": 1,
        "show_content": True,
        "start_at": "2022-12-11 00:00:00",
        "end_at": "2022-12-12 00:00:00",
        "description": "Test Description 1",
        "created_by": 1,
        "is_opened": True,
        "is_recurring": False,
        "cron_expr": None,
        "recurring_end_at": None,
        "recurring_schedule_group": None,
    }

    compare_utils.assert_response_equal(response, status.HTTP_201_CREATED, expected, _EXCEPTION_COLUMNS)


@pytest.mark.django_db
def test_get_wanted_schedule(
    client: test.Client,
    user1: data_utils.UserData,
    user2: data_utils.UserData,
    user3: data_utils.UserData,
):
    client.post(path="/api/v1/user/login/", data=user1.for_login, content_type="application/json")
    schedule_1_data = {
        "participants": [
            {"pk": 3},
        ],
        "title": "Test Schedule 1",
        "protection_level": 1,
        "show_content": True,
        "start_at": "2022-12-11 00:00:00",
        "end_at": "2022-12-12 00:00:00",
        "description": "Test Description 1",
        "is_opened": True,
        "is_recurring": False,
        "cron_expr": None,
        "recurring_end_at": None,
        "recurring_schedule_group": None,
    }
    schedule_2_data = {
        "participants": [
            {"pk": 2},
        ],
        "title": "Test Schedule 2",
        "protection_level": 1,
        "show_content": True,
        "start_at": "2022-12-13 00:00:00",
        "end_at": "2022-12-14 00:00:00",
        "description": "Test Description 2",
        "is_opened": True,
        "is_recurring": False,
        "cron_expr": None,
        "recurring_end_at": None,
        "recurring_schedule_group": None,
    }
    schedule_3_data = {
        "participants": [
            {"pk": 2},
            {"pk": 3},
        ],
        "title": "Test Schedule 3",
        "protection_level": 1,
        "show_content": True,
        "start_at": "2022-12-15 00:00:00",
        "end_at": "2022-12-16 00:00:00",
        "description": "Test Description 3",
        "is_opened": True,
        "is_recurring": False,
        "cron_expr": None,
        "recurring_end_at": None,
        "recurring_schedule_group": None,
    }

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

    target_uri = uri_utils.get_uri_with_extra_params(
        url="/api/v1/calendar/schedule/",
        extra_params={
            "pk": 1,
            "from": "2022-12-13",
            "to": "2022-12-14",
        },
    )
    response = client.get(target_uri)
    expected = [
        {
            "id": 2,
            "participants": [
                {
                    "pk": 2,
                    "username": "user2",
                    "email": "user2@example.com",
                }
            ],
            "title": "Test Schedule 2",
            "protection_level": 1,
            "show_content": True,
            "start_at": "2022-12-13 00:00:00",
            "end_at": "2022-12-14 00:00:00",
            "description": "Test Description 2",
            "is_opened": True,
            "is_recurring": False,
            "cron_expr": None,
            "recurring_end_at": None,
            "created_by": 1,
            "recurring_schedule_group": None,
        }
    ]
    compare_utils.assert_response_equal(response, status.HTTP_200_OK, expected, _EXCEPTION_COLUMNS)


@pytest.mark.django_db
def test_create_recurring_schedule(
    client: test.Client,
    user1: data_utils.UserData,
    user2: data_utils.UserData,
    user3: data_utils.UserData,
):
    client.post(path="/api/v1/user/login/", data=user1.for_login, content_type="application/json")
    schedule_data = {
        "participants": [
            {
                "pk": 2,
            },
            {
                "pk": 3,
            },
        ],
        "title": "Test Schedule 1",
        "protection_level": 1,
        "show_content": True,
        "start_at": "2023-01-23 01:00:00",
        "end_at": "2023-01-23 01:30:00",
        "description": "Test Description 1",
        "is_opened": True,
        "is_recurring": True,
        "cron_expr": "* * * * 1 *",
        "recurring_end_at": "2023-02-10 00:00:00",
    }

    response = client.post(
        path="/api/v1/calendar/schedule/",
        data=schedule_data,
        content_type="application/json",
    )
    expected = {
        "id": 1,
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
        "title": "Test Schedule 1",
        "protection_level": 1,
        "show_content": True,
        "start_at": "2023-01-23 01:00:00",
        "end_at": "2023-01-23 01:30:00",
        "description": "Test Description 1",
        "created_by": 1,
        "is_opened": True,
        "is_recurring": True,
        "cron_expr": "* * * * 1 *",
        "recurring_end_at": "2023-02-10 00:00:00",
        "recurring_schedule_group": 1,
    }

    compare_utils.assert_response_equal(response, status.HTTP_201_CREATED, expected, _EXCEPTION_COLUMNS)
    serializer = calendar_serializers.ScheduleSerializer(
        calendar_models.Schedule.objects.filter(recurring_schedule_group=1),
        many=True,
    )
    child_schedule_1 = copy.deepcopy(expected)
    child_schedule_2 = copy.deepcopy(expected)
    child_schedule_2.update(
        {
            "id": 2,
            "start_at": "2023-01-30 01:00:00",
            "end_at": "2023-01-30 01:30:00",
        }
    )
    child_schedule_3 = copy.deepcopy(expected)
    child_schedule_3.update(
        {
            "id": 3,
            "start_at": "2023-02-06 01:00:00",
            "end_at": "2023-02-06 01:30:00",
        }
    )
    expected_recurring_schedule = [
        child_schedule_1,
        child_schedule_2,
        child_schedule_3,
    ]

    compare_utils.assert_json_equal(serializer.data, expected_recurring_schedule, _EXCEPTION_COLUMNS)
    response = client.get(path="/api/v1/calendar/schedule/group/1/")

    new_data = {
        "start_at": "2023-02-06 02:00:00",
        "end_at": "2023-02-06 02:30:00",
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
        }
    )
    child_schedule_2.update(
        {
            "start_at": "2023-01-30 02:00:00",
            "end_at": "2023-01-30 02:30:00",
        }
    )
    child_schedule_3.update(
        {
            "start_at": "2023-02-06 02:00:00",
            "end_at": "2023-02-06 02:30:00",
        }
    )
    expected_recurring_schedule = [
        child_schedule_1,
        child_schedule_2,
        child_schedule_3,
    ]
    compare_utils.assert_json_equal(response.json()["schedules"], expected_recurring_schedule, _EXCEPTION_COLUMNS)

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


@pytest.mark.django_db
def test_get_schedule_list_open_permission_success(
    client: test.Client,
    user1: data_utils.UserData,
    user2: data_utils.UserData,
):
    client.post("/api/v1/user/login/", data=user2.for_login, content_type="application/json")
    schedule2_data = data_utils.ScheduleData.create_nth_schedule_data(2, protection.ProtectionLevel.OPEN, []).as_dict()
    client.post(
        path="/api/v1/calendar/schedule/",
        data=schedule2_data,
        content_type="application/json",
    )
    schedule3_data = data_utils.ScheduleData.create_nth_schedule_data(3, protection.ProtectionLevel.CLOSED, []).as_dict()
    client.post(
        path="/api/v1/calendar/schedule/",
        data=schedule3_data,
        content_type="application/json",
    )
    schedule3_1_data = data_utils.ScheduleData.create_nth_schedule_data(3, protection.ProtectionLevel.FOLLOWER, []).as_dict()
    client.post(
        path="/api/v1/calendar/schedule/",
        data=schedule3_1_data,
        content_type="application/json",
    )
    client.post("/api/v1/user/logout/")
    client.post("/api/v1/user/login/", data=user1.for_login, content_type="application/json")

    target_uri = uri_utils.get_uri_with_extra_params(
        url="/api/v1/calendar/schedule/",
        extra_params={
            "pk": 2,
            "from": "2022-12-11",
            "to": "2022-12-12",
        },
    )
    response = client.get(target_uri)
    expected = [
        {
            "id": 1,
            "participants": [],
            "title": "Test Schedule 2",
            "protection_level": 1,
            "show_content": True,
            "start_at": "2022-12-11 00:00:00",
            "end_at": "2022-12-12 00:00:00",
            "description": "Test Description 2",
            "created_by": 2,
            "is_opened": True,
            "is_recurring": False,
            "cron_expr": None,
            "recurring_end_at": None,
            "recurring_schedule_group": None,
        }
    ]

    compare_utils.assert_response_equal(response, status.HTTP_200_OK, expected, _EXCEPTION_COLUMNS)


@pytest.mark.django_db
def test_get_schedule_list_follower_permission_success(
    client: test.Client,
    user1: data_utils.UserData,
    user2: data_utils.UserData,
):
    client.post("/api/v1/user/login/", data=user2.for_login, content_type="application/json")

    schedule2_data = dataclasses.asdict(data_utils.ScheduleData.create_nth_schedule_data(2, protection.ProtectionLevel.OPEN, []))
    client.post(
        path="/api/v1/calendar/schedule/",
        data=schedule2_data,
        content_type="application/json",
    )
    schedule3_data = dataclasses.asdict(data_utils.ScheduleData.create_nth_schedule_data(3, protection.ProtectionLevel.CLOSED, []))
    client.post(
        path="/api/v1/calendar/schedule/",
        data=schedule3_data,
        content_type="application/json",
    )
    schedule4_data = dataclasses.asdict(data_utils.ScheduleData.create_nth_schedule_data(4, protection.ProtectionLevel.FOLLOWER, []))
    client.post(
        path="/api/v1/calendar/schedule/",
        data=schedule4_data,
        content_type="application/json",
    )
    client.post("/api/v1/user/logout/")
    client.post("/api/v1/user/login/", data=user1.for_login, content_type="application/json")

    client.post(path="/api/v1/social/network/", data={"followee": {"pk": 2}}, content_type="application/json")
    client.patch(path="/api/v1/social/network/1/", data={"approved": True}, content_type="application/json")

    target_uri = uri_utils.get_uri_with_extra_params(
        url="/api/v1/calendar/schedule/",
        extra_params={
            "pk": 2,
            "from": "2022-12-11",
            "to": "2022-12-12",
        },
    )
    response = client.get(target_uri)
    expected = [
        {
            "id": 1,
            "participants": [],
            "title": "Test Schedule 2",
            "protection_level": 1,
            "show_content": True,
            "start_at": "2022-12-11 00:00:00",
            "end_at": "2022-12-12 00:00:00",
            "description": "Test Description 2",
            "created_by": 2,
            "is_opened": True,
            "is_recurring": False,
            "cron_expr": None,
            "recurring_end_at": None,
            "recurring_schedule_group": None,
        },
        {
            "id": 3,
            "participants": [],
            "title": "Test Schedule 4",
            "protection_level": 2,
            "show_content": True,
            "start_at": "2022-12-11 00:00:00",
            "end_at": "2022-12-12 00:00:00",
            "description": "Test Description 4",
            "created_by": 2,
            "is_opened": True,
            "is_recurring": False,
            "cron_expr": None,
            "recurring_end_at": None,
            "recurring_schedule_group": None,
        },
    ]
    compare_utils.assert_response_equal(response, status.HTTP_200_OK, expected, _EXCEPTION_COLUMNS)


@pytest.mark.django_db
def test_get_unauthorized_schedule_fail(
    client: test.Client,
    user1: data_utils.UserData,
    user2: data_utils.UserData,
):
    """Test of permissions.IsScheduleCreatorrOrReader for non-follower relationship."""
    client.post("/api/v1/user/login/", data=user2.for_login, content_type="application/json")

    schedule1_data = dataclasses.asdict(data_utils.ScheduleData.create_nth_schedule_data(2, protection.ProtectionLevel.FOLLOWER, []))
    client.post(
        path="/api/v1/calendar/schedule/",
        data=schedule1_data,
        content_type="application/json",
    )
    client.post("/api/v1/user/logout/")
    client.post("/api/v1/user/login/", data=user1.for_login, content_type="application/json")

    response = client.get(path="/api/v1/calendar/schedule/1/")
    compare_utils.assert_response_equal(response, status.HTTP_403_FORBIDDEN)


@pytest.mark.django_db
def test_get_follower_schedule_success(
    client: test.Client,
    user1: data_utils.UserData,
    user2: data_utils.UserData,
):
    client.post("/api/v1/user/login/", data=user2.for_login, content_type="application/json")

    schedule1_data = dataclasses.asdict(data_utils.ScheduleData.create_nth_schedule_data(2, protection.ProtectionLevel.FOLLOWER, []))
    client.post(
        path="/api/v1/calendar/schedule/",
        data=schedule1_data,
        content_type="application/json",
    )
    client.post("/api/v1/user/logout/")
    client.post("/api/v1/user/login/", data=user1.for_login, content_type="application/json")

    response = client.post(path="/api/v1/social/network/", data={"followee": {"pk": 2}}, content_type="application/json")
    response = client.patch(path="/api/v1/social/network/1/", data={"approved": True}, content_type="application/json")

    target_uri = uri_utils.get_uri_with_extra_params(
        url="/api/v1/calendar/schedule/1/",
        extra_params={"pk": 2},
    )
    response = client.get(target_uri)

    # TODO: check response body
    compare_utils.assert_response_equal(response, status.HTTP_200_OK)


@pytest.mark.django_db
def test_get_follower_schedule_fail(
    client: test.Client,
    user1: data_utils.UserData,
    user2: data_utils.UserData,
):
    client.post("/api/v1/user/login/", data=user2.for_login, content_type="application/json")

    schedule1_data = dataclasses.asdict(data_utils.ScheduleData.create_nth_schedule_data(2, protection.ProtectionLevel.FOLLOWER, []))
    client.post(
        path="/api/v1/calendar/schedule/",
        data=schedule1_data,
        content_type="application/json",
    )
    client.post("/api/v1/user/logout/")
    client.post("/api/v1/user/login/", data=user1.for_login, content_type="application/json")

    target_uri = uri_utils.get_uri_with_extra_params(
        url="/api/v1/calendar/schedule/1/",
        extra_params={"pk": 2},
    )

    response = client.get(target_uri)
    compare_utils.assert_response_equal(response, status.HTTP_403_FORBIDDEN)


@pytest.mark.django_db
def test_update_schedule(
    client: test.Client,
    user1: data_utils.UserData,
    user2: data_utils.UserData,
):
    client.post("/api/v1/user/login/", data=user1.for_login, content_type="application/json")
    client.post(
        path="/api/v1/calendar/schedule/",
        data={
            "title": "Test Schedule 1-1",
            "start_at": "2022-12-11 00:00:00",
            "end_at": "2022-12-12 00:00:00",
            "description": "Test description 1-1",
        },
        content_type="application/json",
    )

    # Check Patch (Partial Update)
    response = client.patch(
        path="/api/v1/calendar/schedule/1/",
        data={"title": "Modified Test Schedule 1-1"},
        content_type="application/json",
    )
    expected = {
        "id": 1,
        "participants": [],
        "title": "Modified Test Schedule 1-1",
        "protection_level": 1,
        "show_content": True,
        "start_at": "2022-12-11 00:00:00",
        "end_at": "2022-12-12 00:00:00",
        "description": "Test description 1-1",
        "created_by": 1,
        "is_opened": True,
        "is_recurring": False,
        "cron_expr": None,
        "recurring_end_at": None,
        "recurring_schedule_group": None,
    }
    compare_utils.assert_response_equal(response, status.HTTP_200_OK, expected, _EXCEPTION_COLUMNS)

    # Check Put (Total Update)
    response = client.put(
        path="/api/v1/calendar/schedule/1/",
        data={
            "title": "Second Modified Test Schedule 1-1",
            "start_at": "2022-12-12 00:00:00",
            "end_at": "2022-12-13 00:00:00",
            "description": "Second Modified Test description 1-1",
        },
        content_type="application/json",
    )
    expected = {
        "id": 1,
        "participants": [],
        "title": "Second Modified Test Schedule 1-1",
        "protection_level": 1,
        "show_content": True,
        "start_at": "2022-12-12 00:00:00",
        "end_at": "2022-12-13 00:00:00",
        "description": "Second Modified Test description 1-1",
        "created_by": 1,
        "is_opened": True,
        "is_recurring": False,
        "cron_expr": None,
        "recurring_end_at": None,
        "recurring_schedule_group": None,
    }
    compare_utils.assert_response_equal(response, status.HTTP_200_OK, expected, _EXCEPTION_COLUMNS)

    # Check Delete
    response = client.delete(path="/api/v1/calendar/schedule/1/", content_type="application/json")
    compare_utils.assert_response_equal(response, status.HTTP_204_NO_CONTENT)

    response = client.get(path="/api/v1/calendar/schedule/1/", content_type="application/json")
    compare_utils.assert_response_equal(response, status.HTTP_404_NOT_FOUND)


@pytest.mark.django_db
def test_attendance_success(
    client: test.Client,
    user1: data_utils.UserData,
    user2: data_utils.UserData,
    user3: data_utils.UserData,
):
    client.post(path="/api/v1/user/login/", data=user1.for_login, content_type="application/json")

    schedule1_data = dataclasses.asdict(data_utils.ScheduleData.create_nth_schedule_data(1, protection.ProtectionLevel.FOLLOWER, [2, 3]))
    response = client.post(
        path="/api/v1/calendar/schedule/",
        data=schedule1_data,
        content_type="application/json",
    )

    client.post("/api/v1/user/logout/")
    client.post("/api/v1/user/login/", data=user2.for_login, content_type="application/json")

    # check attendance
    response = client.patch(
        path="/api/v1/calendar/schedule/1/attendance/",
        data={"status": 3},
        content_type="application/json",
    )
    expected = {"id": 1, "status": 3, "participant": 2, "schedule": 1}

    compare_utils.assert_response_equal(response, status.HTTP_200_OK, expected, _EXCEPTION_COLUMNS)


@pytest.mark.django_db
def test_attendance_fail(
    client: test.Client,
    user1: data_utils.UserData,
    user2: data_utils.UserData,
    user3: data_utils.UserData,
):
    client.post(path="/api/v1/user/login/", data=user1.for_login, content_type="application/json")

    schedule1_data = dataclasses.asdict(data_utils.ScheduleData.create_nth_schedule_data(1, protection.ProtectionLevel.FOLLOWER, [2, 3]))
    response = client.post(
        path="/api/v1/calendar/schedule/",
        data=schedule1_data,
        content_type="application/json",
    )

    # check attendance
    response = client.patch(
        path="/api/v1/calendar/schedule/1/attendance/",
        data={"status": 3},
        content_type="application/json",
    )
    compare_utils.assert_response_equal(response, status.HTTP_404_NOT_FOUND)


@pytest.mark.django_db
def test_attendance_read_only_fields_fail(
    client: test.Client,
    user1: data_utils.UserData,
    user2: data_utils.UserData,
    user3: data_utils.UserData,
):
    client.post(path="/api/v1/user/login/", data=user1.for_login, content_type="application/json")

    schedule1_data = dataclasses.asdict(data_utils.ScheduleData.create_nth_schedule_data(1, protection.ProtectionLevel.FOLLOWER, [2, 3]))
    response = client.post(
        path="/api/v1/calendar/schedule/",
        data=schedule1_data,
        content_type="application/json",
    )

    client.post("/api/v1/user/logout/")
    client.post("/api/v1/user/login/", data=user2.for_login, content_type="application/json")

    # check attendance
    response = client.patch(
        path="/api/v1/calendar/schedule/1/attendance/",
        data={"status": 3, "id": 100},
        content_type="application/json",
    )
    expected = {"id": 1, "status": 3, "participant": 2, "schedule": 1}

    compare_utils.assert_response_equal(response, status.HTTP_200_OK, expected, _EXCEPTION_COLUMNS)
