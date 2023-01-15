from django.db import models

from calendar_j.services.attendance import attendance
from calendar_j.services.protection import protection
from user import models as user_models


class Schedule(models.Model):
    title = models.CharField(max_length=250)
    created_by = models.ForeignKey(user_models.User, on_delete=models.PROTECT, related_name="schedules")
    protection_level = models.IntegerField(
        choices=protection.ProtectionLevel.choices,
        default=protection.ProtectionLevel.get_default(),
    )
    show_content = models.BooleanField(default=True, blank=True)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    participants = models.ManyToManyField(user_models.User, through="Participant")
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_opened = models.BooleanField(default=True, blank=True)

    class Meta:
        verbose_name = "schedule"
        verbose_name_plural = "schedules"
        db_table = "tb_schedule"


class Participant(models.Model):
    participant = models.ForeignKey(user_models.User, on_delete=models.PROTECT)
    schedule = models.ForeignKey(Schedule, on_delete=models.PROTECT)
    status = models.IntegerField(
        choices=attendance.AttendanceStatus.choices,
        default=attendance.AttendanceStatus.get_default(),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "participant"
        verbose_name_plural = "participants"
        db_table = "tb_participant"


class RecurringSchedule(models.Model):
    recurring = models.OneToOneField(Schedule, on_delete=models.PROTECT, primary_key=True)
    cron_exp = models.CharField(max_length=10)
    end_date = models.DateField()
