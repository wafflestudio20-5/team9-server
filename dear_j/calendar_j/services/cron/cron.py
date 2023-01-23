from django.db import models

"cron_rule": {
    "basic_type":DAILY.
    "interval":n, 
    "day_of_week":"mon,tue,wed",
    "monthly_type":"date"/"last_date"/"day",
    "yearly_type":"date"/"day"/"last_date",
    "monthly_date":"7/27",
    "monthly_day":"3thMON",
    "yearly_date":"7/3/MON",
    "yearly_day":"7/"
    "value":"7/27", "3/mon", "7/3/mon", "7"
}

class CronBasicType(models.IntegerChoices):
    DAILY = 1
    WEEKLY = 2
    MONTHLY = 3
    YEARLY = 4

class CronIntervalType(models.IntegerChoices):
    EVERY = 1

class CronWeeklyType(models.IntegerChoices):
    MON = 1
    TUE = 2
    WED = 3
    THR = 4
    FRI = 5
    SAT = 6
    SUN = 7

class CronMonthlyType(models.IntegerChoices):
    DATE = 1
    DAY = 2
    LAST_DATE = 3

class CronYearlyType(models.IntegerChoices):
    DATE = 1
    DAY = 2
    LAST_DATE = 3
