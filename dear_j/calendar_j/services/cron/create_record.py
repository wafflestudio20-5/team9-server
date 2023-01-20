from django.db import models

import datetime
from dateutil import relativedelta
from typing import List
from typing import Tuple

from calendar_j import models
from calendar_j.services.cron import cron

cron.CronBasicType

class CreateCronRecord:
    def get_interval(cls, cron_type: int) -> relativedelta.relativedelta:
        if cron_type == cron.CronBasicType.DAY:
            return relativedelta.relativedelta(days=1)
        if cron_type == cron.CronBasicType.WEEK:
            return relativedelta.relativedelta(weeks=1)
        if cron_type == cron.CronBasicType.MONTH:
            return relativedelta.relativedelta(months=1)
        if cron_type == cron.CronBasicType.YEAR:
            return relativedelta.relativedelta(years=1)

    def create_record(cls, cron_rule: models.RecurringRecord, schedule: models.Schedule) -> List[Tuple[datetime.datetime, datetime.datetime]]:
        output = []
        interval = cls.get_interval(cron_rule.cron)
        start_at = schedule.start_at + interval
        end_at = schedule.end_at + interval
        while cron_rule.end_at <= cron_rule.end_date:
            output.append((start_at, end_at))
            start_at += interval
            end_at += interval
        return output
