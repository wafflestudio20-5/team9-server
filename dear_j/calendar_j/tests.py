from rest_framework import status
from rest_framework import test

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

        response = self.client.post(
            path="/api/v1/calendar/schedule/",
            data={
                "title": "Test Schedule1",
                "start_at": "2022-12-11 00:00:00",
                "end_at": "2022-12-12 00:00:00",
                "description": "Test description",
                "participants": [
                    {
                        "pk": 2,
                    },
                    {
                        "pk": 3,
                    },
                ],
            },
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
            "title": "Test Schedule1",
            "protection_level": 1,
            "start_at": "2022-12-11 00:00:00",
            "end_at": "2022-12-12 00:00:00",
            "description": "Test description",
            "created_by": 1,
        }
        actual = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for key, value in expected.items():
            assert key in actual.keys()
            assert actual[key] == value

    def test_get_schedule_list_success(self):
        user1_data = test_data_utils.UserData.create_nth_user_data(1)
        user2_data = test_data_utils.UserData.create_nth_user_data(2)

        self.client.post("/api/v1/user/registration/", data=user1_data.for_registration, format="json")
        self.client.post("/api/v1/user/registration/", data=user2_data.for_registration, format="json")

        self.client.post("/api/v1/user/login/", data=user2_data.for_login, format="json")
        self.client.post(
            path="/api/v1/calendar/schedule/",
            data={
                "title": "Test Schedule 2",
                "start_at": "2022-12-11 00:00:00",
                "end_at": "2022-12-12 00:00:00",
                "description": "Test description 2",
                "participants": [
                    {
                        "pk": 1,
                    },
                ],
            },
            format="json",
        )
        self.client.post(
            path="/api/v1/calendar/schedule/",
            data={
                "title": "Test Schedule 3",
                "start_at": "2022-12-11 00:00:00",
                "end_at": "2022-12-12 00:00:00",
                "description": "Test description 3",
            },
            format="json",
        )
        self.client.post("/api/v1/user/logout/")
        self.client.post("/api/v1/user/login/", data=user1_data.for_login, format="json")

        self.client.post(
            path="/api/v1/calendar/schedule/",
            data={
                "title": "Test Schedule 1",
                "start_at": "2022-12-13 00:00:00",
                "end_at": "2022-12-14 00:00:00",
                "description": "Test description 1",
                "participants": [
                    {
                        "pk": 2,
                    },
                ],
            },
            format="json",
        )
        target_uri = uri_utils.get_uri_with_extra_params(
            url="/api/v1/calendar/schedule/",
            extra_params={
                "email": user1_data.email,
                "from": "2022-12-11",
                "to": "2022-12-12",
            },
        )
        response = self.client.get(target_uri)
        expected = [
            {
                "id": 1,
                "participants": [
                    {
                        "pk": 1,
                        "username": "user1",
                        "email": "user1@example.com",
                    }
                ],
                "title": "Test Schedule 2",
                "protection_level": 1,
                "start_at": "2022-12-11 00:00:00",
                "end_at": "2022-12-12 00:00:00",
                "description": "Test description 2",
                "created_by": 2,
            },
        ]
        actual = response.json()["results"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for actual_row, expected_row in zip(actual, expected):
            for key, value in expected_row.items():
                assert key in actual_row.keys()
                assert actual_row[key] == value

    def test_get_schedule_list_fail(self):
        user1_data = test_data_utils.UserData.create_nth_user_data(1)
        user2_data = test_data_utils.UserData.create_nth_user_data(2)

        self.client.post("/api/v1/user/registration/", data=user1_data.for_registration, format="json")
        self.client.post("/api/v1/user/registration/", data=user2_data.for_registration, format="json")

        self.client.post("/api/v1/user/login/", data=user2_data.for_login, format="json")
        self.client.post(
            path="/api/v1/calendar/schedule/",
            data={
                "title": "Test Schedule 2",
                "start_at": "2022-12-11 00:00:00",
                "end_at": "2022-12-12 00:00:00",
                "description": "Test description 2",
                "protection_level": protection.ProtectionLevel.CLOSED,
                "participants": [
                    {
                        "pk": 1,
                    },
                ],
            },
            format="json",
        )
        self.client.post("/api/v1/user/logout/")
        self.client.post("/api/v1/user/login/", data=user1_data.for_login, format="json")

        target_uri = uri_utils.get_uri_with_extra_params(
            url="/api/v1/calendar/schedule/1/",
            extra_params={"email": user2_data.email},
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

    def test_attendence_success(self):
        creator_data = test_data_utils.UserData.create_nth_user_data(1)
        participant1_data = test_data_utils.UserData.create_nth_user_data(2)
        participant2_data = test_data_utils.UserData.create_nth_user_data(3)

        self.client.post(path="/api/v1/user/registration/", data=creator_data.for_registration, format="json")
        self.client.post(path="/api/v1/user/registration/", data=participant1_data.for_registration, format="json")
        self.client.post(path="/api/v1/user/registration/", data=participant2_data.for_registration, format="json")
        self.client.post(path="/api/v1/user/login/", data=creator_data.for_login, format="json")

        response = self.client.post(
            path="/api/v1/calendar/schedule/",
            data={
                "title": "Test Schedule1",
                "start_at": "2022-12-11 00:00:00",
                "end_at": "2022-12-12 00:00:00",
                "description": "Test description",
                "participants": [
                    {
                        "pk": 2,
                    },
                    {
                        "pk": 3,
                    },
                ],
            },
            format="json",
        )

        self.client.post("/api/v1/user/logout/")
        self.client.post("/api/v1/user/login/", data=participant1_data.for_login, format="json")

        # check attendence
        response = self.client.patch(
            path="/api/v1/calendar/schedule/1/attendence/",
            data={"status": 3},
            format="json",
        )

        expected = {"id": 1, "status": 3, "participant": 2, "schedule": 1}
        actual = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for key, value in expected.items():
            assert key in actual.keys()
            assert actual[key] == value

    def test_attendence_fail(self):
        creator_data = test_data_utils.UserData.create_nth_user_data(1)
        participant1_data = test_data_utils.UserData.create_nth_user_data(2)
        participant2_data = test_data_utils.UserData.create_nth_user_data(3)

        self.client.post(path="/api/v1/user/registration/", data=creator_data.for_registration, format="json")
        self.client.post(path="/api/v1/user/registration/", data=participant1_data.for_registration, format="json")
        self.client.post(path="/api/v1/user/registration/", data=participant2_data.for_registration, format="json")
        self.client.post(path="/api/v1/user/login/", data=creator_data.for_login, format="json")

        response = self.client.post(
            path="/api/v1/calendar/schedule/",
            data={
                "title": "Test Schedule1",
                "start_at": "2022-12-11 00:00:00",
                "end_at": "2022-12-12 00:00:00",
                "description": "Test description",
                "participants": [
                    {
                        "pk": 2,
                    },
                    {
                        "pk": 3,
                    },
                ],
            },
            format="json",
        )

        # check attendence
        response = self.client.patch(
            path="/api/v1/calendar/schedule/1/attendence/",
            data={"status": 3},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
