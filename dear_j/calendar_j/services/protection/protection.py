from django.db import models

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
    def filter_user_schedule(cls, request_user: user_models.User, target_pk: int) -> int:
        target_user = user_models.User.objects.get(pk=target_pk)
        if social_models.Network.objects.filter(follower=request_user, followee=target_user).first():
            return cls.FOLLOWER
        return cls.OPEN

    @classmethod
    def allow_request_user(cls, protection_level: int, request_user: user_models.User, target_user: user_models.User) -> bool:
        if target_user == request_user or protection_level == cls.OPEN:
            return True
        if protection_level == cls.FOLLOWER:
            if social_models.Network.objects.filter(follower=request_user, followee=target_user).first() is not None:
                return True
        return False
