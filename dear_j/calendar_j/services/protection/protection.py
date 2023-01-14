from django.db import models as django_models

from calendar_j import models as calendar_models
from social import models as social_models
from user import models as user_models


class ProtectionLevel(django_models.IntegerChoices):
    OPEN = 1
    FOLLOWER = 2
    CLOSED = 3

    @classmethod
    def get_default(cls):
        return cls.OPEN.value

    @classmethod
    def get_allowed_threshold(cls, request_user, target_email):
        target_user = user_models.User.objects.get(email=target_email)
        if social_models.Network.objects.filter(follower=request_user, followee=target_user).first() is not None:
            return cls.FOLLOWER
        return cls.OPEN
