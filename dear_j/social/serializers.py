from typing import Dict

from django import shortcuts
from rest_framework import serializers

from social import exceptions as social_exceptions
from social import models as social_models
from user import models as user_models
from user import serializers as user_serializers


class NetworkSerializer(serializers.ModelSerializer):
    followee = user_serializers.EssentialUserInfoFromPKSerializer(many=False, required=True)

    class Meta:
        model = social_models.Network
        fields = "__all__"
        extra_kwargs = {
            "follower": {
                "default": serializers.CurrentUserDefault(),
            },
        }

    def create(self, validated_data) -> social_models.Network:
        follower = self.context.get("request").user
        followee = shortcuts.get_object_or_404(user_models.User, pk=validated_data["followee"]["pk"])
        network = social_models.Network.objects.create(
            follower=follower,
            followee=followee,
        )
        return network

    def update(self, instance: social_models.Network, validated_data: Dict):
        for key in validated_data.keys():
            if key != "approved":
                raise social_exceptions.FollowAcceptOrRejectAPIException
        return super().update(instance, validated_data)
