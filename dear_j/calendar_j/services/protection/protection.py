from django.db import models


class ProtectionLevel(models.IntegerChoices):
    OPEN = 1
    OPEN_TO_FOLLOWER = 2
    SEMI_OPEN_TO_FOLLOWER = 3  # busy
    CLOSED = 4

    @classmethod
    def get_default(cls):
        return cls.OPEN.value
