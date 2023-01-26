import dataclasses
import datetime
import enum
from typing import Any, Dict, Tuple, Union

from dateutil import relativedelta

from rest_framework import exceptions


@dataclasses.dataclass
class Cron:
    position: int
    step_size: Union[datetime.timedelta, relativedelta.relativedelta]
    usability: bool = True


_MINUTE = Cron(
    position=0,
    step_size=datetime.timedelta(minutes=1),
    usability=False,
)

_HOUR = Cron(
    position=1,
    step_size=datetime.timedelta(hours=1),
    usability=False,
)

_DAY_OF_MONTH = Cron(
    position=2,
    step_size=datetime.timedelta(days=1),
)

_MONTH = Cron(
    position=3,
    step_size=relativedelta.relativedelta(months=1),
)

_DAY_OF_WEEK = Cron(
    position=4,
    step_size=datetime.timedelta(weeks=1),
)

_YEAR = Cron(
    position=5,
    step_size=relativedelta.relativedelta(years=1),
)


class CronInfo(enum.Enum):
    MINUTE = _MINUTE
    HOUR = _HOUR
    DAY_OF_MONTH = _DAY_OF_MONTH
    MONTH = _MONTH
    DAY_OF_WEEK = _DAY_OF_WEEK
    YEAR = _YEAR

    def __init__(self, info: Cron) -> None:
        self.unit_position = info.position
        self.unit_step_size = info.step_size
        self.unit_usability = info.usability

    @classmethod
    def _parse_cron(cls, position: int, cron_data: str) -> Dict[str, Any]:
        if position == cls.DAY_OF_WEEK.unit_position:
            if "/" in cron_data:
                days_of_week, num_steps = cron_data.split("/")
            else:
                days_of_week = cron_data
                num_steps = 1
            if all(j in [f"{i}" for i in range(0, 8)] for j in days_of_week.split(",")):
                return {
                    "days_of_week": [int(i) for i in days_of_week.split(",")],
                    "num_steps": int(num_steps),
                }

        if cron_data.startswith("*/"):
            try:
                return {"num_steps": int(cron_data[2:])}
            except ValueError as e:
                raise exceptions.ValidationError(e)
        raise exceptions.ValidationError("Not proper cron expression")

    @classmethod
    def _get_unit(cls, position: int) -> Cron:
        for info in cls:
            if position == info.unit_position:
                return info.value
        raise exceptions.ValidationError("Not proper cron expression")

    @classmethod
    def parse(cls, cron_expr: str) -> Tuple[Cron, Dict[str, Any]]:
        cron_list = cron_expr.split(" ")

        position = None
        data = None
        for position, data in enumerate(cron_list):
            if data != "*":
                unit = cls._get_unit(position)
                break

        if (not position) or (not data):
            raise exceptions.ValidationError("Not proper cron expression")

        parsed_data = cls._parse_cron(position, data)
        return unit, parsed_data


def apply_recurring_rule(
    cron_expr: str,
    parent_start_at: datetime.datetime,
    parent_end_at: datetime.datetime,
    recurring_end_at: datetime.datetime,
):
    cron_unit, parsed_data = CronInfo.parse(cron_expr)
    interval = cron_unit.step_size * parsed_data.get("num_steps")

    if cron_unit == CronInfo.DAY_OF_WEEK.value:
        child_start_at_list = []
        child_end_at_list = []

        # The day of week of start_day
        start_day_of_week = parent_start_at.weekday() + 1
        for target_date_of_week in parsed_data.get("days_of_week"):
            delta = target_date_of_week - start_day_of_week

            if delta > 0:
                child_start_at = parent_start_at + delta * datetime.timedelta(days=1)
                child_end_at = parent_end_at + delta * datetime.timedelta(days=1)
            if delta < 0:
                child_start_at = parent_start_at + (delta + 7) * datetime.timedelta(days=1)
                child_end_at = parent_end_at + (delta + 7) * datetime.timedelta(days=1)
            if delta == 0:
                child_start_at = parent_start_at
                child_end_at = parent_end_at

            child_start_at_list.append(child_start_at)
            child_end_at_list.append(child_end_at)
    else:
        child_start_at_list = [parent_start_at]
        child_end_at_list = [parent_end_at]

    start_at_list = []
    end_at_list = []

    for child_start_at, child_end_at in zip(child_start_at_list, child_end_at_list):
        while child_start_at < recurring_end_at:
            start_at_list.append(child_start_at)
            end_at_list.append(child_end_at)

            child_start_at += interval
            child_end_at += interval

    return sorted(start_at_list), sorted(end_at_list)
