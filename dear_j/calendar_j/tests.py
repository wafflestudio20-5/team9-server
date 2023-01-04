from __future__ import annotations

import dataclasses
from typing import Dict

from rest_framework import status
from rest_framework import test


@dataclasses.dataclass
class UserData:
    username: str
    email: str
    password: str
    birthdate: str

    @property
    def for_registration(self) -> Dict:
        return {
            "username": self.username,
            "email": self.email,
            "password1": self.password,
            "password2": self.password,
            "birthdate": self.birthdate,
        }

    @property
    def for_login(self) -> Dict:
        return {
            "email": self.email,
            "password": self.password,
        }

    @classmethod
    def create_nth_user_data(cls, n: int) -> UserData:
        return cls(
            username=f"user{n}",
            email=f"user{n}@example.com",
            password=f"password@{n}",
            birthdate="2000-01-01",
        )


class CalendarAPITest(test.APITestCase):
    def setUp(self) -> None:
        self.client = test.APIClient(enforce_csrf_checks=False)

    def test_create_schedule(self):
        creator_data = UserData.create_nth_user_data(1)
        participant1_data = UserData.create_nth_user_data(2)
        participant2_data = UserData.create_nth_user_data(3)

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
                        "email": "user2@example.com",
                    },
                    {
                        "email": "user3@example.com",
                    },
                ],
            },
            format="json",
        )
        expected = {
            "id": 1,
            "participants": [
                {"email": "user2@example.com"},
                {"email": "user3@example.com"},
            ],
            "title": "Test Schedule1",
            "protection_level": 1,
            "start_at": "2022-12-11T00:00:00Z",
            "end_at": "2022-12-12T00:00:00Z",
            "description": "Test description",
            "created_by": 1,
        }
        actual = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for key, value in expected.items():
            assert key in actual.keys()
            assert actual[key] == value

    def test_get_schedule_list(self):
        user1_data = UserData.create_nth_user_data(1)
        user2_data = UserData.create_nth_user_data(2)

        self.client.post("/api/v1/user/registration/", data=user1_data.for_registration, format="json")
        self.client.post("/api/v1/user/registration/", data=user2_data.for_registration, format="json")

        self.client.post("/api/v1/user/login/", data=user1_data.for_login, format="json")

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

        self.client.post(
            path="/api/v1/calendar/schedule/",
            data={
                "title": "Test Schedule 2",
                "start_at": "2022-12-12 00:00:00",
                "end_at": "2022-12-13 00:00:00",
                "description": "Test description 2",
                "participants": [
                    {
                        "email": "user2@example.com",
                    },
                ],
            },
            format="json",
        )

        response = self.client.get("/api/v1/calendar/schedule/")

        expected = [
            {
                "id": 1,
                "participants": [],
                "title": "Test Schedule 1-1",
                "protection_level": 1,
                "start_at": "2022-12-11T00:00:00Z",
                "end_at": "2022-12-12T00:00:00Z",
                "description": "Test description 1-1",
                "created_by": 1,
            },
            {
                "id": 2,
                "participants": [{"email": "user2@example.com"}],
                "title": "Test Schedule 2",
                "protection_level": 1,
                "start_at": "2022-12-12T00:00:00Z",
                "end_at": "2022-12-13T00:00:00Z",
                "description": "Test description 2",
                "created_by": 1,
            },
        ]
        actual = response.json()["results"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for actual_row, expected_row in zip(actual, expected):
            for key, value in expected_row.items():
                assert key in actual_row.keys()
                assert actual_row[key] == value

    def test_update_schedule(self):
        user1_data = UserData.create_nth_user_data(1)
        user2_data = UserData.create_nth_user_data(2)

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
            "start_at": "2022-12-11T00:00:00Z",
            "end_at": "2022-12-12T00:00:00Z",
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
            "start_at": "2022-12-12T00:00:00Z",
            "end_at": "2022-12-13T00:00:00Z",
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
