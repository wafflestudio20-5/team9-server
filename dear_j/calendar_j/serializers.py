from typing import Dict, List, Optional

from rest_framework import exceptions
from rest_framework import fields
from rest_framework import serializers

from calendar_j import models as calendar_model
from calendar_j.services.recurring import cron
from user import models as user_models
from user import serializers as user_serializers


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = calendar_model.Participant
        fields = ["id", "status", "participant", "schedule"]
        read_only_fields = (
            "id",
            "participant",
            "schedule",
        )


class ScheduleFromPKSerializer(serializers.ModelSerializer):
    class Meta:
        model = calendar_model.Schedule
        fields = "__all__"
        read_only_fields = (
            "title",
            "start_at",
            "end_at",
            "created_by",
            "protection_level",
            "show_content",
            "start_at",
            "end_at",
            "participants",
            "description",
            "created_at",
            "updated_at",
            "is_opened",
            "is_recurring",
            "cron_expr",
            "recurring_end_at",
            "recurring_schedule_group",
        )

    def create(self, validated_data: Dict) -> calendar_model.Schedule:
        raise NotImplementedError


class ScheduleSerializer(serializers.ModelSerializer):
    participants = user_serializers.EssentialUserInfoFromPKSerializer(many=True, required=False)

    class Meta:
        model = calendar_model.Schedule
        fields = "__all__"
        extra_kwargs = {
            "created_by": {
                "default": serializers.CurrentUserDefault(),
            },
        }

    def create_participants_with_schedule(
        self,
        schedule: calendar_model.Schedule,
        user_ids: List[int],
    ) -> List[Optional[calendar_model.Participant]]:
        participants = []
        candidates = user_models.User.objects.filter(id__in=user_ids)

        for candidate in candidates:
            if candidate != schedule.created_by:
                participant = calendar_model.Participant.objects.create(schedule=schedule, participant=candidate)
                participants.append(participant)

        return participants

    def create(self, validated_data: Dict) -> calendar_model.Schedule:
        participants_raw_data = validated_data.pop("participants", [])
        user_ids = [row.get("pk") for row in participants_raw_data]

        if validated_data.get("is_recurring"):
            if not any(validated_data.get(key) for key in ("cron_expr", "recurring_end_at")):
                raise exceptions.ValidationError(
                    "cron_expr, recurring_end_at must be defined, " "if you want to create recurring schedule."
                )

        schedule: calendar_model.Schedule = super().create(validated_data)
        self.create_participants_with_schedule(schedule, user_ids)

        schedules = [schedule]
        if schedule.is_recurring:
            start_at_list, end_at_list = cron.apply_recurring_rule(
                schedule.cron_expr,
                schedule.start_at,
                schedule.end_at,
                schedule.recurring_end_at,
            )

            for child_start_at, child_end_at in zip(start_at_list[1:], end_at_list[1:]):
                child_data = validated_data.copy()
                child_data.update(
                    {
                        "start_at": child_start_at,
                        "end_at": child_end_at,
                    }
                )

                child_schedule = super().create(child_data)
                self.create_participants_with_schedule(child_schedule, user_ids)
                schedules.append(child_schedule)

            recurring_schedule_group = calendar_model.RecurringScheduleGroup.objects.create(
                name="recurring_schedule_group",
                created_by=schedule.created_by,
            )
            for child_schedule in schedules:
                child_schedule.recurring_schedule_group = recurring_schedule_group
                child_schedule.save()

        return schedules

    def update(self, instance: calendar_model.Schedule, validated_data: Dict) -> calendar_model.Schedule:
        edit_participants = validated_data.keys().__contains__("participants")
        if edit_participants:
            participants_raw_data = validated_data.pop("participants", [])
            user_ids = [row.get("pk") for row in participants_raw_data]

        schedule = super().update(instance, validated_data)

        if edit_participants:
            participants = calendar_model.Participant.objects.filter(schedule=schedule)
            participants.delete()

            self.create_participants_with_schedule(schedule, user_ids)
        return schedule


class RecurringScheduleGroupSerializer(serializers.ModelSerializer):
    schedules = ScheduleSerializer(many=True)

    class Meta:
        model = calendar_model.RecurringScheduleGroup
        fields = "__all__"
