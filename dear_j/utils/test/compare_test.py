import dataclasses
from typing import Dict, List, Union

from rest_framework import status

from utils.test import compare as compare_utils


@dataclasses.dataclass
class MockResponse:
    data: Union[Dict, List]
    status_code: int

    def json(self):
        return self.data


def test_assert_response_equal():
    response = MockResponse(
        data={
            "id": 1,
            "participants": [
                {"pk": 2, "username": "user2", "email": "user2@example.com"},
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
            "created_at": "2023-01-24 15:10:30",
            "updated_at": "2023-01-24 15:10:30",
            "is_opened": True,
            "is_recurring": True,
            "cron_expr": "* * * * 1 *",
            "recurring_end_at": "2023-02-10 00:00:00",
            "created_by": 1,
            "schedule_groups": [1],
        },
        status_code=status.HTTP_201_CREATED,
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
        "schedule_groups": [1],
    }

    compare_utils.assert_response_equal(response, status.HTTP_201_CREATED, expected, ("created_at", "updated_at"))
