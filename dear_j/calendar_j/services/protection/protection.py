from django.db import models


class ProtectionLevel(models.IntegerChoices):
    OPEN = 1
    SEMI_OPEN = 2
    CLOSED = 3

    @classmethod
    def get_default(cls):
        return cls.OPEN.value
