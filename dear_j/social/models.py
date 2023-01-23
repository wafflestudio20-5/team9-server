from django.db import models

from user import models as user_models


class Network(models.Model):
    follower = models.ForeignKey(user_models.User, on_delete=models.PROTECT, related_name="start_node")
    followee = models.ForeignKey(user_models.User, on_delete=models.PROTECT, related_name="end_node")
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "network"
        verbose_name_plural = "networks"
        db_table = "tb_network"

class Group(models.Model):
    participants = models.ManyToManyField(user_models.User, through="Participants")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "group"
        verbose_name_plural = "groups"
        db_table = "tb_group"
