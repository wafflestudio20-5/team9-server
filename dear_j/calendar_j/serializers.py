from typing import Dict, List, Optional

from rest_framework import exceptions
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
        participants_data: List,
    ) -> List[Optional[calendar_model.Participant]]:
        participants = []

        for participant_data in participants_data:
            target_user = user_models.User.objects.get(**participant_data)

            if target_user != schedule.created_by:
                participant = calendar_model.Participant.objects.create(schedule=schedule, participant=target_user)
                participants.append(participant)

        return participants

    def create(self, validated_data: Dict) -> calendar_model.Schedule:
        participants_data = validated_data.pop("participants", [])
        if validated_data.get("is_recurring"):
            if not any(validated_data.get(key) for key in ("cron_expr", "recurring_end_at")):
                raise exceptions.ValidationError(
                    "cron_expr, recurring_end_at must be defined, " "if you want to create recurring schedule."
                )

        schedule: calendar_model.Schedule = super().create(validated_data)
        self.create_participants_with_schedule(schedule, participants_data)

        if schedule.is_recurring:
            schedules = [schedule]
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
                self.create_participants_with_schedule(child_schedule, participants_data)
                schedules.append(child_schedule)

            group = calendar_model.ScheduleGroup.objects.create(
                name="recurring_schedule_group",
                created_by=schedule.created_by,
            )
            for group_schedule in schedules:
                calendar_model.ScheduleToGroup.objects.create(schedule=group_schedule, group=group)

        return schedule


class ScheduleGroupSerializer(serializers.ModelSerializer):
    schedules = ScheduleSerializer(many=True)

    class Meta:
        model = calendar_model.ScheduleGroup
        fields = "__all__"
