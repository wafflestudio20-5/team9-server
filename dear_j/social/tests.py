from rest_framework import status
from rest_framework import test

from utils import test_data as test_data_utils


class CalendarAPITest(test.APITestCase):
    def setUp(self):
        self.client = test.APIClient(enforce_csrf_checks=False)

    def test_search_candidate(self):
        user1_data = test_data_utils.UserData.create_nth_user_data(1)
        user2_data = test_data_utils.UserData.create_nth_user_data(2)
        user3_data = test_data_utils.UserData.create_nth_user_data(3)
        user4_data = test_data_utils.UserData.create_nth_user_data(4)

        self.client.post(path="/api/v1/user/registration/", data=user1_data.for_registration, format="json")
        self.client.post(path="/api/v1/user/registration/", data=user2_data.for_registration, format="json")
        self.client.post(path="/api/v1/user/registration/", data=user3_data.for_registration, format="json")
        self.client.post(path="/api/v1/user/registration/", data=user4_data.for_registration, format="json")

        response = self.client.get(path="/api/v1/social/search/candidate/?search=user")
        expected = [
            {"pk": 1, "email": "user1@example.com"},
            {"pk": 2, "email": "user2@example.com"},
            {"pk": 3, "email": "user3@example.com"},
            {
                "pk": 4,
                "email": "user4@example.com",
            },
        ]
        actual = response.json()["results"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for actual_row, expected_row in zip(actual, expected):
            for key, value in expected_row.items():
                assert key in actual_row.keys()
                assert actual_row[key] == value

        response = self.client.get(path="/api/v1/social/search/candidate/?search=user3")
        expected = [
            {
                "pk": 3,
                "email": "user3@example.com",
            },
        ]
        actual = response.json()["results"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for actual_row, expected_row in zip(actual, expected):
            for key, value in expected_row.items():
                assert key in actual_row.keys()
                assert actual_row[key] == value

    def test_create_network(self):
        follower_data = test_data_utils.UserData.create_nth_user_data(1)
        followee_data = test_data_utils.UserData.create_nth_user_data(2)

        self.client.post(path="/api/v1/user/registration/", data=follower_data.for_registration, format="json")
        self.client.post(path="/api/v1/user/registration/", data=followee_data.for_registration, format="json")

        self.client.post(path="/api/v1/user/login/", data=follower_data.for_login, format="json")

        response = self.client.post(path="/api/v1/social/network/", data={"followee": {"email": followee_data.email}}, format="json")
        expected = {
            "id": 1,
            "followee": {
                "pk": 2,
                "email": "user2@example.com",
            },
            "approved": False,
            "follower": 1,
        }
        actual = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for key, value in expected.items():
            assert key in actual.keys()
            assert actual[key] == value

        self.client.post(path="/api/v1/user/logout/")
        self.client.post(path="/api/v1/user/login/", data=followee_data.for_login, format="json")

        response = self.client.patch(path="/api/v1/social/network/1/", data={"approved": True}, format="json")
        expected = {
            "id": 1,
            "followee": {
                "pk": 2,
                "email": "user2@example.com",
            },
            "approved": True,
            "is_opened": True,
            "follower": 1,
        }
        actual = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for key, value in expected.items():
            assert key in actual.keys()
            assert actual[key] == value
