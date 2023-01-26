import datetime

from calendar_j.services.recurring import cron


def test_cron():
    start_at = datetime.datetime(2023, 1, 1, 1, 0)
    end_at = datetime.datetime(2023, 1, 1, 3, 0)

    day_cron_expr = "* * */2 * * *"
    recurring_end_at = datetime.datetime(2023, 1, 7)

    start_at_list, end_at_list = cron.apply_recurring_rule(day_cron_expr, start_at, end_at, recurring_end_at)
    expected_start_at_list = [
        start_at,
        start_at + datetime.timedelta(days=2),
        start_at + datetime.timedelta(days=4),
        start_at + datetime.timedelta(days=6),
    ]
    expected_end_at_list = [
        end_at,
        end_at + datetime.timedelta(days=2),
        end_at + datetime.timedelta(days=4),
        end_at + datetime.timedelta(days=6),
    ]

    assert start_at_list == expected_start_at_list
    assert end_at_list == expected_end_at_list

    month_cron_expr = "* * * */1 * *"
    recurring_end_at = datetime.datetime(2023, 2, 10)

    start_at_list, end_at_list = cron.apply_recurring_rule(month_cron_expr, start_at, end_at, recurring_end_at)
    expected_start_at_list = [
        datetime.datetime(2023, 1, 1, 1, 0),
        datetime.datetime(2023, 2, 1, 1, 0),
    ]
    expected_end_at_list = [
        datetime.datetime(2023, 1, 1, 3, 0),
        datetime.datetime(2023, 2, 1, 3, 0),
    ]

    assert start_at_list == expected_start_at_list
    assert end_at_list == expected_end_at_list

    year_cron_expr = "* * * * * */1"
    recurring_end_at = datetime.datetime(2024, 4, 10)

    start_at_list, end_at_list = cron.apply_recurring_rule(year_cron_expr, start_at, end_at, recurring_end_at)
    expected_start_at_list = [
        datetime.datetime(2023, 1, 1, 1, 0),
        datetime.datetime(2024, 1, 1, 1, 0),
    ]
    expected_end_at_list = [
        datetime.datetime(2023, 1, 1, 3, 0),
        datetime.datetime(2024, 1, 1, 3, 0),
    ]

    assert start_at_list == expected_start_at_list
    assert end_at_list == expected_end_at_list

    monday_cron_expr = "* * * * 1 *"
    recurring_end_at = datetime.datetime(2023, 1, 21)

    start_at_list, end_at_list = cron.apply_recurring_rule(monday_cron_expr, start_at, end_at, recurring_end_at)
    expected_start_at_list = [
        datetime.datetime(2023, 1, 2, 1, 0),
        datetime.datetime(2023, 1, 9, 1, 0),
        datetime.datetime(2023, 1, 16, 1, 0),
    ]
    expected_end_at_list = [
        datetime.datetime(2023, 1, 2, 3, 0),
        datetime.datetime(2023, 1, 9, 3, 0),
        datetime.datetime(2023, 1, 16, 3, 0),
    ]

    assert start_at_list == expected_start_at_list
    assert end_at_list == expected_end_at_list

    monday_and_wednesday_cron_expr = "* * * * 1,3 *"
    recurring_end_at = datetime.datetime(2023, 1, 14)

    start_at_list, end_at_list = cron.apply_recurring_rule(monday_and_wednesday_cron_expr, start_at, end_at, recurring_end_at)
    expected_start_at_list = [
        datetime.datetime(2023, 1, 2, 1, 0),
        datetime.datetime(2023, 1, 4, 1, 0),
        datetime.datetime(2023, 1, 9, 1, 0),
        datetime.datetime(2023, 1, 11, 1, 0),
    ]
    expected_end_at_list = [
        datetime.datetime(2023, 1, 2, 3, 0),
        datetime.datetime(2023, 1, 4, 3, 0),
        datetime.datetime(2023, 1, 9, 3, 0),
        datetime.datetime(2023, 1, 11, 3, 0),
    ]

    assert start_at_list == expected_start_at_list
    assert end_at_list == expected_end_at_list

    monday_and_wednesday_cron_per_two_weeks_expr = "* * * * 1,3/2 *"
    recurring_end_at = datetime.datetime(2023, 1, 20)

    start_at_list, end_at_list = cron.apply_recurring_rule(monday_and_wednesday_cron_per_two_weeks_expr, start_at, end_at, recurring_end_at)
    expected_start_at_list = [
        datetime.datetime(2023, 1, 2, 1, 0),
        datetime.datetime(2023, 1, 4, 1, 0),
        datetime.datetime(2023, 1, 16, 1, 0),
        datetime.datetime(2023, 1, 18, 1, 0),
    ]
    expected_end_at_list = [
        datetime.datetime(2023, 1, 2, 3, 0),
        datetime.datetime(2023, 1, 4, 3, 0),
        datetime.datetime(2023, 1, 16, 3, 0),
        datetime.datetime(2023, 1, 18, 3, 0),
    ]

    assert start_at_list == expected_start_at_list
    assert end_at_list == expected_end_at_list
