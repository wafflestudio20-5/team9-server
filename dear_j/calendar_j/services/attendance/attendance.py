from django.db import models


class AttendanceStatus(models.IntegerChoices):
    PRESENCE = 1
    ABSENCE = 2
    HOLD = 3
    UNANSWERED = 4

    @staticmethod
    def get_default():
        return AttendanceStatus.UNANSWERED.value
