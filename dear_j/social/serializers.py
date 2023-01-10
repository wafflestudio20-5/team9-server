from django import shortcuts
from rest_framework import serializers

from social import models as social_models
from user import models as user_models
from user import serializers as user_serializers


class NetworkSerializer(serializers.ModelSerializer):
    # TODO: Followee can only update approve state to True when is_opened=True
    followee = user_serializers.UserEmailSerializer(many=False, required=True)

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
        followee = shortcuts.get_object_or_404(user_models.User, email=validated_data["followee"]["email"])
        network = social_models.Network.objects.create(
            follower=follower,
            followee=followee,
        )
        return network
