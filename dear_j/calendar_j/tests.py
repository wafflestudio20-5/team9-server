import dataclasses

from rest_framework import status
from rest_framework import test

from calendar_j.services.cron import cron
from calendar_j.services.protection import protection
from utils import test_data as test_data_utils
from utils import uri as uri_utils


class CalendarAPITest(test.APITestCase):
    def setUp(self) -> None:
        self.client = test.APIClient(enforce_csrf_checks=False)

    def test_create_schedule(self):
        creator_data = test_data_utils.UserData.create_nth_user_data(1)
        participant1_data = test_data_utils.UserData.create_nth_user_data(2)
        participant2_data = test_data_utils.UserData.create_nth_user_data(3)

        self.client.post(path="/api/v1/user/registration/", data=creator_data.for_registration, format="json")
        self.client.post(path="/api/v1/user/registration/", data=participant1_data.for_registration, format="json")
        self.client.post(path="/api/v1/user/registration/", data=participant2_data.for_registration, format="json")
        self.client.post(path="/api/v1/user/login/", data=creator_data.for_login, format="json")

        schedule_data = dataclasses.asdict(test_data_utils.ScheduleData.create_nth_calendar_data(1, 1, [2, 3]))
        response = self.client.post(
            path="/api/v1/calendar/schedule/",
            data=schedule_data,
            format="json",
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
            "start_at": "2022-12-11 00:00:00",
            "end_at": "2022-12-12 00:00:00",
            "description": "Test Description 1",
            "created_by": 1,
        }
        actual = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for key, value in expected.items():
            if key not in actual.keys():
                print(key)
            assert key in actual.keys()
            assert actual[key] == value

    def test_get_schedule_list_open_permission_success(self):
        user1_data = test_data_utils.UserData.create_nth_user_data(1)
        user2_data = test_data_utils.UserData.create_nth_user_data(2)

        self.client.post("/api/v1/user/registration/", data=user1_data.for_registration, format="json")
        self.client.post("/api/v1/user/registration/", data=user2_data.for_registration, format="json")

        self.client.post("/api/v1/user/login/", data=user2_data.for_login, format="json")
        schedule2_data = dataclasses.asdict(test_data_utils.ScheduleData.create_nth_calendar_data(2, protection.ProtectionLevel.OPEN, []))
        self.client.post(
            path="/api/v1/calendar/schedule/",
            data=schedule2_data,
            format="json",
        )
        schedule3_data = dataclasses.asdict(test_data_utils.ScheduleData.create_nth_calendar_data(3, protection.ProtectionLevel.CLOSED, []))
        self.client.post(
            path="/api/v1/calendar/schedule/",
            data=schedule3_data,
            format="json",
        )
        schedule3_1_data = dataclasses.asdict(
            test_data_utils.ScheduleData.create_nth_calendar_data(3, protection.ProtectionLevel.FOLLOWER, [])
        )
        self.client.post(
            path="/api/v1/calendar/schedule/",
            data=schedule3_1_data,
            format="json",
        )
        self.client.post("/api/v1/user/logout/")
        self.client.post("/api/v1/user/login/", data=user1_data.for_login, format="json")

        target_uri = uri_utils.get_uri_with_extra_params(
            url="/api/v1/calendar/schedule/",
            extra_params={
                "pk": 2,
                "from": "2022-12-11",
                "to": "2022-12-12",
            },
        )
        response = self.client.get(target_uri)
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
            }
        ]
        actual = response.json()["results"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for actual_row, expected_row in zip(actual, expected):
            for key, value in expected_row.items():
                assert key in actual_row.keys()
                if key not in ["created_at", "updated_at"]:
                    assert actual_row[key] == value

    def test_get_schedule_list_follower_permission_success(self):
        user1_data = test_data_utils.UserData.create_nth_user_data(1)
        user2_data = test_data_utils.UserData.create_nth_user_data(2)

        self.client.post("/api/v1/user/registration/", data=user1_data.for_registration, format="json")
        self.client.post("/api/v1/user/registration/", data=user2_data.for_registration, format="json")

        self.client.post("/api/v1/user/login/", data=user2_data.for_login, format="json")

        schedule2_data = dataclasses.asdict(test_data_utils.ScheduleData.create_nth_calendar_data(2, protection.ProtectionLevel.OPEN, []))
        self.client.post(
            path="/api/v1/calendar/schedule/",
            data=schedule2_data,
            format="json",
        )
        schedule3_data = dataclasses.asdict(test_data_utils.ScheduleData.create_nth_calendar_data(3, protection.ProtectionLevel.CLOSED, []))
        self.client.post(
            path="/api/v1/calendar/schedule/",
            data=schedule3_data,
            format="json",
        )
        schedule4_data = dataclasses.asdict(
            test_data_utils.ScheduleData.create_nth_calendar_data(4, protection.ProtectionLevel.FOLLOWER, [])
        )
        self.client.post(
            path="/api/v1/calendar/schedule/",
            data=schedule4_data,
            format="json",
        )
        self.client.post("/api/v1/user/logout/")
        self.client.post("/api/v1/user/login/", data=user1_data.for_login, format="json")

        response = self.client.post(path="/api/v1/social/network/", data={"followee": {"pk": 2}}, format="json")
        response = self.client.patch(path="/api/v1/social/network/1/", data={"approved": True}, format="json")

        target_uri = uri_utils.get_uri_with_extra_params(
            url="/api/v1/calendar/schedule/",
            extra_params={
                "pk": 2,
                "from": "2022-12-11",
                "to": "2022-12-12",
            },
        )
        response = self.client.get(target_uri)
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
            },
        ]
        actual = response.json()["results"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for actual_row, expected_row in zip(actual, expected):
            for key, value in expected_row.items():
                assert key in actual_row.keys()
                if key not in ["created_at", "updated_at"]:
                    assert actual_row[key] == value

    def test_get_closed_schedule_fail(self):
        user1_data = test_data_utils.UserData.create_nth_user_data(1)
        user2_data = test_data_utils.UserData.create_nth_user_data(2)

        self.client.post("/api/v1/user/registration/", data=user1_data.for_registration, format="json")
        self.client.post("/api/v1/user/registration/", data=user2_data.for_registration, format="json")

        self.client.post("/api/v1/user/login/", data=user2_data.for_login, format="json")

        schedule1_data = dataclasses.asdict(
            test_data_utils.ScheduleData.create_nth_calendar_data(2, protection.ProtectionLevel.FOLLOWER, [])
        )
        self.client.post(
            path="/api/v1/calendar/schedule/",
            data=schedule1_data,
            format="json",
        )
        self.client.post("/api/v1/user/logout/")
        self.client.post("/api/v1/user/login/", data=user1_data.for_login, format="json")

        target_uri = uri_utils.get_uri_with_extra_params(
            url="/api/v1/calendar/schedule/1/",
            extra_params={"pk": 2},
        )
        response = self.client.get(target_uri)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_follower_schedule_success(self):
        user1_data = test_data_utils.UserData.create_nth_user_data(1)  # follower
        user2_data = test_data_utils.UserData.create_nth_user_data(2)  # followee

        self.client.post("/api/v1/user/registration/", data=user1_data.for_registration, format="json")
        self.client.post("/api/v1/user/registration/", data=user2_data.for_registration, format="json")

        self.client.post("/api/v1/user/login/", data=user2_data.for_login, format="json")

        schedule1_data = dataclasses.asdict(
            test_data_utils.ScheduleData.create_nth_calendar_data(2, protection.ProtectionLevel.FOLLOWER, [])
        )
        self.client.post(
            path="/api/v1/calendar/schedule/",
            data=schedule1_data,
            format="json",
        )
        self.client.post("/api/v1/user/logout/")
        self.client.post("/api/v1/user/login/", data=user1_data.for_login, format="json")

        response = self.client.post(path="/api/v1/social/network/", data={"followee": {"pk": 2}}, format="json")
        response = self.client.patch(path="/api/v1/social/network/1/", data={"approved": True}, format="json")

        target_uri = uri_utils.get_uri_with_extra_params(
            url="/api/v1/calendar/schedule/1/",
            extra_params={"pk": 2},
        )
        response = self.client.get(target_uri)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_follower_schedule_fail(self):
        user1_data = test_data_utils.UserData.create_nth_user_data(1)
        user2_data = test_data_utils.UserData.create_nth_user_data(2)

        self.client.post("/api/v1/user/registration/", data=user1_data.for_registration, format="json")
        self.client.post("/api/v1/user/registration/", data=user2_data.for_registration, format="json")

        self.client.post("/api/v1/user/login/", data=user2_data.for_login, format="json")

        schedule1_data = dataclasses.asdict(
            test_data_utils.ScheduleData.create_nth_calendar_data(2, protection.ProtectionLevel.FOLLOWER, [])
        )
        self.client.post(
            path="/api/v1/calendar/schedule/",
            data=schedule1_data,
            format="json",
        )
        self.client.post("/api/v1/user/logout/")
        self.client.post("/api/v1/user/login/", data=user1_data.for_login, format="json")

        target_uri = uri_utils.get_uri_with_extra_params(
            url="/api/v1/calendar/schedule/1/",
            extra_params={"pk": 2},
        )
        response = self.client.get(target_uri)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_schedule(self):
        user1_data = test_data_utils.UserData.create_nth_user_data(1)
        user2_data = test_data_utils.UserData.create_nth_user_data(2)

        self.client.post("/api/v1/user/registration/", data=user1_data.for_registration, format="json")
        self.client.post("/api/v1/user/registration/", data=user2_data.for_registration, format="json")

        self.client.post("/api/v1/user/login/", data=user1_data.for_login, format="json")
        pk = (
            self.client.post(
                path="/api/v1/calendar/schedule/",
                data={
                    "title": "Test Schedule 1-1",
                    "start_at": "2022-12-11 00:00:00",
                    "end_at": "2022-12-12 00:00:00",
                    "description": "Test description 1-1",
                },
                format="json",
            )
            .json()
            .get("id")
        )

        # Check Patch (Partial Update)
        response = self.client.patch(path=f"/api/v1/calendar/schedule/{pk}/", data={"title": "Modified Test Schedule 1-1"}, format="json")
        expected = {
            "id": 1,
            "participants": [],
            "title": "Modified Test Schedule 1-1",
            "protection_level": 1,
            "start_at": "2022-12-11 00:00:00",
            "end_at": "2022-12-12 00:00:00",
            "description": "Test description 1-1",
            "created_by": 1,
        }
        actual = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for key, value in expected.items():
            assert key in actual.keys()
            assert actual[key] == value

        # Check Put (Total Update)
        response = self.client.put(
            path=f"/api/v1/calendar/schedule/{pk}/",
            data={
                "title": "Second Modified Test Schedule 1-1",
                "start_at": "2022-12-12 00:00:00",
                "end_at": "2022-12-13 00:00:00",
                "description": "Second Modified Test description 1-1",
            },
            format="json",
        )
        expected = {
            "id": 1,
            "participants": [],
            "title": "Second Modified Test Schedule 1-1",
            "protection_level": 1,
            "start_at": "2022-12-12 00:00:00",
            "end_at": "2022-12-13 00:00:00",
            "description": "Second Modified Test description 1-1",
            "created_by": 1,
        }
        actual = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for key, value in expected.items():
            assert key in actual.keys()
            assert actual[key] == value

        # Check Delete
        response = self.client.delete(path=f"/api/v1/calendar/schedule/{pk}/", format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_attendance_success(self):
        creator_data = test_data_utils.UserData.create_nth_user_data(1)
        participant1_data = test_data_utils.UserData.create_nth_user_data(2)
        participant2_data = test_data_utils.UserData.create_nth_user_data(3)

        self.client.post(path="/api/v1/user/registration/", data=creator_data.for_registration, format="json")
        self.client.post(path="/api/v1/user/registration/", data=participant1_data.for_registration, format="json")
        self.client.post(path="/api/v1/user/registration/", data=participant2_data.for_registration, format="json")
        self.client.post(path="/api/v1/user/login/", data=creator_data.for_login, format="json")

        schedule1_data = dataclasses.asdict(
            test_data_utils.ScheduleData.create_nth_calendar_data(1, protection.ProtectionLevel.FOLLOWER, [2, 3])
        )
        response = self.client.post(
            path="/api/v1/calendar/schedule/",
            data=schedule1_data,
            format="json",
        )

        self.client.post("/api/v1/user/logout/")
        self.client.post("/api/v1/user/login/", data=participant1_data.for_login, format="json")

        # check attendance
        response = self.client.patch(
            path="/api/v1/calendar/schedule/1/attendance/",
            data={"status": 3},
            format="json",
        )

        expected = {"id": 1, "status": 3, "participant": 2, "schedule": 1}
        actual = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for key, value in expected.items():
            assert key in actual.keys()
            assert actual[key] == value

    def test_attendance_fail(self):
        creator_data = test_data_utils.UserData.create_nth_user_data(1)
        participant1_data = test_data_utils.UserData.create_nth_user_data(2)
        participant2_data = test_data_utils.UserData.create_nth_user_data(3)

        self.client.post(path="/api/v1/user/registration/", data=creator_data.for_registration, format="json")
        self.client.post(path="/api/v1/user/registration/", data=participant1_data.for_registration, format="json")
        self.client.post(path="/api/v1/user/registration/", data=participant2_data.for_registration, format="json")
        self.client.post(path="/api/v1/user/login/", data=creator_data.for_login, format="json")

        schedule1_data = dataclasses.asdict(
            test_data_utils.ScheduleData.create_nth_calendar_data(1, protection.ProtectionLevel.FOLLOWER, [2, 3])
        )
        response = self.client.post(
            path="/api/v1/calendar/schedule/",
            data=schedule1_data,
            format="json",
        )

        # check attendance
        response = self.client.patch(
            path="/api/v1/calendar/schedule/1/attendance/",
            data={"status": 3},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_attendance_read_only_fields_fail(self):
        creator_data = test_data_utils.UserData.create_nth_user_data(1)
        participant1_data = test_data_utils.UserData.create_nth_user_data(2)
        participant2_data = test_data_utils.UserData.create_nth_user_data(3)

        self.client.post(path="/api/v1/user/registration/", data=creator_data.for_registration, format="json")
        self.client.post(path="/api/v1/user/registration/", data=participant1_data.for_registration, format="json")
        self.client.post(path="/api/v1/user/registration/", data=participant2_data.for_registration, format="json")
        self.client.post(path="/api/v1/user/login/", data=creator_data.for_login, format="json")

        schedule1_data = dataclasses.asdict(
            test_data_utils.ScheduleData.create_nth_calendar_data(1, protection.ProtectionLevel.FOLLOWER, [2, 3])
        )
        response = self.client.post(
            path="/api/v1/calendar/schedule/",
            data=schedule1_data,
            format="json",
        )

        self.client.post("/api/v1/user/logout/")
        self.client.post("/api/v1/user/login/", data=participant1_data.for_login, format="json")

        # check attendance
        response = self.client.patch(
            path="/api/v1/calendar/schedule/1/attendance/",
            data={"status": 3, "id": 100},
            format="json",
        )

        expected = {"id": 1, "status": 3, "participant": 2, "schedule": 1}
        actual = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for key, value in expected.items():
            assert key in actual.keys()
            assert actual[key] == value

    def test_create_recurring_schedule(self):
        creator_data = test_data_utils.UserData.create_nth_user_data(1)
        participant1_data = test_data_utils.UserData.create_nth_user_data(2)
        participant2_data = test_data_utils.UserData.create_nth_user_data(3)

        self.client.post(path="/api/v1/user/registration/", data=creator_data.for_registration, format="json")
        self.client.post(path="/api/v1/user/registration/", data=participant1_data.for_registration, format="json")
        self.client.post(path="/api/v1/user/registration/", data=participant2_data.for_registration, format="json")
        self.client.post(path="/api/v1/user/login/", data=creator_data.for_login, format="json")

        schedule_data = dataclasses.asdict(
            test_data_utils.ScheduleData.create_recurring_calendar_data(1, 1, [2, 3], cron.CronBasicType.DAY, "2023-01-02"))
        response = self.client.post(
            path="/api/v1/calendar/schedule/",
            data=schedule_data,
            format="json",
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
            "start_at": "2022-12-11 00:00:00",
            "end_at": "2022-12-12 00:00:00",
            "description": "Test Description 1",
            "created_by": 1,
        }
        actual = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for key, value in expected.items():
            if key not in actual.keys():
                print(key)
            assert key in actual.keys()
            assert actual[key] == value

    def test_get_recurring_schedule(self):
        creator_data = test_data_utils.UserData.create_nth_user_data(1)
        participant1_data = test_data_utils.UserData.create_nth_user_data(2)
        participant2_data = test_data_utils.UserData.create_nth_user_data(3)

        self.client.post(path="/api/v1/user/registration/", data=creator_data.for_registration, format="json")
        self.client.post(path="/api/v1/user/registration/", data=participant1_data.for_registration, format="json")
        self.client.post(path="/api/v1/user/registration/", data=participant2_data.for_registration, format="json")
        self.client.post(path="/api/v1/user/login/", data=creator_data.for_login, format="json")

        schedule_data = dataclasses.asdict(
            test_data_utils.ScheduleData.create_recurring_calendar_data(1, 1, [2, 3], cron.CronBasicType.DAY.value, "2022-12-14"))
        response = self.client.post(
            path="/api/v1/calendar/schedule/",
            data=schedule_data,
            format="json",
        )

        target_uri = uri_utils.get_uri_with_extra_params(
            url="/api/v1/calendar/schedule/",
            extra_params={
                "pk": 1,
                "from": "2022-12-10",
                "to": "2022-12-30",
            },
        )
        response = self.client.get(target_uri)
        print(response.json())

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
            "start_at": "2022-12-11 00:00:00",
            "end_at": "2022-12-12 00:00:00",
            "description": "Test Description 1",
            "created_by": 1,
        }
        actual = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for key, value in expected.items():
            if key not in actual.keys():
                print(key)
            assert key in actual.keys()
            assert actual[key] == value
