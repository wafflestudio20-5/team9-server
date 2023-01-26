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
    show_content = models.BooleanField(default=True, null=False)
    start_at = models.DateTimeField(null=False)
    end_at = models.DateTimeField(null=False)
    participants = models.ManyToManyField(user_models.User, through="Participant")
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_opened = models.BooleanField(default=True, null=False)
    is_recurring = models.BooleanField(default=False, null=False)
    cron_expr = models.CharField(null=True, max_length=100)
    recurring_end_at = models.DateTimeField(null=True)
    recurring_schedule_group = models.ForeignKey("RecurringScheduleGroup", null=True, on_delete=models.PROTECT, related_name="schedules")

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


class RecurringScheduleGroup(models.Model):
    name = models.CharField(null=True, max_length=100)
    is_opened = models.BooleanField(default=True, null=False)
    created_by = models.ForeignKey(user_models.User, on_delete=models.PROTECT, related_name="recurring_schedule_groups")

    class Meta:
        verbose_name = "recurring_schedule_group"
        verbose_name_plural = "recurring_schedule_groups"
        db_table = "tb_recurring_schedule_group"
