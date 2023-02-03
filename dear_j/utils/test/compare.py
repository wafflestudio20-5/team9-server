from typing import Dict, List, Optional, Union

from rest_framework import response as resp


def assert_json_equal(
    actual: Union[Dict, List],
    expected: Union[Dict, List],
    exception_columns: Optional[List[str]] = ("created_at", "updated_at"),
):
    if not exception_columns:
        exception_columns = []

    if isinstance(actual, dict):
        assert isinstance(expected, dict), "Data type is different."
        actual = [actual]
        expected = [expected]

    assert len(actual) == len(expected), "Response Length is different. " f"Actual: {len(actual)} || Expected: {len(expected)}"

    for actual_row, expected_row in zip(actual, expected):
        for key, value in actual_row.items():
            if key not in exception_columns:
                assert key in expected_row.keys(), f"{key} is not in expected"
                assert expected_row[key] == value, f"Value of {key} is different. " f"Actual: {value} || Expected: {expected_row[key]}"


def assert_response_equal(
    response: resp.Response,
    expected_status_code: int,
    expected: Optional[Union[Dict, List]] = None,
    exception_columns: Optional[List[str]] = ("created_at", "updated_at"),
):
    if not exception_columns:
        exception_columns = []

    assert response.status_code == expected_status_code, (
        f"Status Code is different. " f"Actual: {response.status_code} || Expected: {expected_status_code}"
    )

    if expected:
        actual: Union[Dict, List] = response.json()

        if isinstance(actual, Dict) and "results" in actual.keys():
            actual = actual.get("results")

        assert_json_equal(actual, expected, exception_columns)
