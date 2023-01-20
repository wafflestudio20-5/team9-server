from typing import Dict

from rest_framework import serializers

from calendar_j import models as calendar_model
from calendar_j.services.cron import cron
from calendar_j.services.cron import create_record
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

class RecurringRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = calendar_model.RecurringRule
        fields = "__all__"

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

    def create(self, validated_data: Dict) -> calendar_model.Schedule:
        participants_data = validated_data.pop("participants", [])
        schedule = super().create(validated_data)
        recurring_rule = validated_data.pop("recurring_rule", [])

        for participant_data in participants_data:
            participant = user_models.User.objects.get(**participant_data)
            if participant != self.context["request"].user:
                calendar_model.Participant.objects.create(schedule=schedule, participant=participant)

        if recurring_rule != []:
            cron = recurring_rule.pop("cron_exp", None)
            end_date = recurring_rule.pop("end_date", None)
            if cron is not None and end_date is not None:
                recurring = calendar_model.RecurringRule.objects.create(
                    schedule=schedule, cron=cron, end_date=end_date)
                for (start_at, end_at) in create_record.CreateCronRecord.create_record(cron, schedule):
                    calendar_model.RecurringRecord.objects.create(
                        schedule=schedule, start_at=start_at, end_at=end_at
                    )
            else:
                raise serializers.ValidationError("wrong recurring_rule request")
        return schedule
