from django.db import models


class CronBasicType(models.IntegerChoices):
    DAY = 1
    WEEK = 2
    MONTH = 3
    YEAR = 4

class CronWeeklyType(models.IntegerChoices):
    MON = 1
    TUE = 2
    WED = 3
    THR = 4
    FRI = 5
    SAT = 6
    SUN = 7
