from typing import Dict

from rest_framework import serializers

from calendar_j import models as calendar_model
from user import models as user_models
from user import serializers as user_serializers


class ParticipantEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def create(self, validated_data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        raise NotImplementedError


class ScheduleSerializer(serializers.ModelSerializer):
    participants = user_serializers.UserEmailSerializer(many=True, required=False)

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
            calendar_model.Participant.objects.create(schedule=schedule, participant=participant)
        return schedule


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = calendar_model.Participant
        fields = "__all__"
