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


@pytest.fixture(name="user3")
def fixture_registered_user3(client: test.Client):
    user3_data = data_utils.UserData.create_nth_user_data(3)
    client.post(path="/api/v1/user/registration/", data=user3_data.for_registration, content_type="application/json")
    return user3_data


@pytest.mark.django_db
def test_attendance_success(
    client: test.Client,
    user1: data_utils.UserData,
    user2: data_utils.UserData,
    user3: data_utils.UserData,
):
    """Test Schedule Attendance Update API"""
    client.post(path="/api/v1/user/login/", data=user1.for_login, content_type="application/json")

    schedule1_data = data_utils.ScheduleData.create_nth_schedule_data(
        n=1, protection_level=protection.ProtectionLevel.FOLLOWER, participant_ids=[2, 3]
    ).as_dict()
    client.post(
        path="/api/v1/calendar/schedule/",
        data=schedule1_data,
        content_type="application/json",
    )

    # Cannot Update
    response = client.patch(
        path="/api/v1/calendar/schedule/1/attendance/",
        data={"status": attendance.AttendanceStatus.HOLD},
        content_type="application/json",
    )
    compare_utils.assert_response_equal(response, status.HTTP_404_NOT_FOUND)

    client.post("/api/v1/user/logout/")
    client.post("/api/v1/user/login/", data=user2.for_login, content_type="application/json")

    # Can Update
    response = client.patch(
        path="/api/v1/calendar/schedule/1/attendance/",
        data={"status": attendance.AttendanceStatus.HOLD},
        content_type="application/json",
    )
    expected = {"id": 1, "status": attendance.AttendanceStatus.HOLD, "participant": 2, "schedule": 1}

    compare_utils.assert_response_equal(response, status.HTTP_200_OK, expected)
