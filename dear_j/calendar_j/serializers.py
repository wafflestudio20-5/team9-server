from typing import Dict

from rest_framework import serializers

from calendar_j import models as calendar_model
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

    def create(self, validated_data: Dict) -> calendar_model.Schedule:
        participants_data = validated_data.pop("participants", [])
        schedule = super().create(validated_data)

        for participant_data in participants_data:
            participant = user_models.User.objects.get(**participant_data)
            if participant != self.context["request"].user:
                calendar_model.Participant.objects.create(schedule=schedule, participant=participant)
        return schedule
