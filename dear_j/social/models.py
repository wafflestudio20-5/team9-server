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
