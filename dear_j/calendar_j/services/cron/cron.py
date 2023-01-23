from django.db import models


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

class CronYearlyType(models.IntegerChoices):
    MONTH_DATE = 1
    MONTH_DAY = 2
