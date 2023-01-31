from django.db import models
from rest_framework import exceptions

from social import models as social_models
from user import models as user_models


class ProtectionLevel(models.IntegerChoices):
    OPEN = 1
    FOLLOWER = 2
    CLOSED = 3

    @classmethod
    def get_default(cls):
        return cls.OPEN.value

    @classmethod
    def filter_user_schedule(cls, request_user: user_models.User, target_user: user_models.User) -> int:
        if request_user == target_user:
            return cls.CLOSED
        if social_models.Network.objects.filter(follower=request_user, followee=target_user):
            return cls.FOLLOWER
        return cls.OPEN

    @classmethod
    def allow_request_user(cls, protection_level: int, request_user: user_models.User, target_user: user_models.User) -> bool:
        if protection_level == cls.OPEN:
            return True
        if protection_level == cls.FOLLOWER:
            if social_models.Network.objects.filter(follower=request_user, followee=target_user):
                return True
            return False
        if protection_level == cls.CLOSED:
            return target_user == request_user
        raise exceptions.ValidationError("protection_level must be one of ProtectionLevel value")
