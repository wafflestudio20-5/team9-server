import datetime

from utils import time as time_utils


def test_replace_time():
    origin = datetime.datetime(2022, 1, 1)
    new = datetime.datetime(2022, 1, 1, 2, 30)
    assert time_utils.replace_time(origin, new) == datetime.datetime(2022, 1, 1, 2, 30)

    origin = datetime.datetime(2022, 1, 7)
    new = datetime.datetime(2022, 1, 1, 2, 30)
    assert time_utils.replace_time(origin, new) == datetime.datetime(2022, 1, 7, 2, 30)


def test_normal_date_formatter():
    normal_date = datetime.date(2023, 1, 1)
    normal_date_str = "2023-01-01"

    assert time_utils.normal_date_formatter.format(normal_date) == normal_date_str
    assert time_utils.normal_date_formatter.parse(normal_date_str) == normal_date


def test_normal_datetime_formatter():
    normal_datetime = datetime.datetime(2023, 1, 1, 1, 30, 0)
    normal_datetime_str = "2023-01-01 01:30:00"

    assert time_utils.normal_datetime_formatter.format(normal_datetime) == normal_datetime_str
    assert time_utils.normal_datetime_formatter.parse(normal_datetime_str) == normal_datetime


def test_compact_date_formatter():
    compact_date = datetime.date(2023, 1, 1)
    compact_date_str = "20230101"

    assert time_utils.compact_date_formatter.format(compact_date) == compact_date_str
    assert time_utils.compact_date_formatter.parse(compact_date_str) == compact_date
