from django.db import models

from user import models as user_models


class ProtectionLevel(models.IntegerChoices):
    OPEN = 1
    SEMI_OPEN = 2
    CLOSED = 3

    DEFAULT = OPEN


class Schedule(models.Model):
    title = models.CharField(max_length=50)
    created_by = models.ForeignKey(user_models.User, on_delete=models.PROTECT)
    protection_level = models.IntegerField(
        choices=ProtectionLevel.choices,
        default=ProtectionLevel.DEFAULT.value,
    )
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    participants = models.ManyToManyField(user_models.User, through="Participant")
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    url = models.URLField(blank=True)

    class Meta:
        verbose_name = "schedule"
        verbose_name_plural = "schedules"
        db_table = "tb_schedule"


class AttendanceStatus(models.IntegerChoices):
    PRESENCE = 1
    ABSENCE = 2
    HOLD = 3
    UNANSWERED = 4

    DEFAULT = UNANSWERED


class Participant(models.Model):
    participant = models.ForeignKey(user_models.User, on_delete=models.PROTECT)
    schedule = models.ForeignKey(Schedule, on_delete=models.PROTECT)
    status = models.IntegerField(
        choices=AttendanceStatus.choices,
        default=AttendanceStatus.DEFAULT.value,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "participant"
        verbose_name_plural = "participants"
        db_table = "tb_participant"
