import pytest

from rest_framework import test


def _create_test_client() -> test.APIClient:
    return test.APIClient()


@pytest.fixture(scope="session")
def client():
    test_client = _create_test_client()
    test_client.enforce_csrf_checks = False
    yield test_client
