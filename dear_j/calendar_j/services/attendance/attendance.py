from django.db import models


class AttendanceStatus(models.IntegerChoices):
    PRESENCE = 1
    ABSENCE = 2
    HOLD = 3
    UNANSWERED = 4

    @classmethod
    def get_default(cls):
        return cls.UNANSWERED.value
