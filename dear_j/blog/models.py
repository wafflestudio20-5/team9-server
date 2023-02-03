from django.db import models

from calendar_j import models as calendar_models
from user import models as user_models


class Post(models.Model):
    title = models.CharField(max_length=50)
    created_by = models.ForeignKey(user_models.User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField()
    image = models.ImageField(upload_to="post", editable=True, null=True)
    schedules = models.ManyToManyField(calendar_models.Schedule, through="ScheduleToPost", blank=True)

    class Meta:
        verbose_name = "post"
        verbose_name_plural = "posts"
        db_table = "tb_post"

    def __str__(self):
        return str(self.title)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_by = models.ForeignKey(user_models.User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_updated = models.BooleanField(default=False)
    content = models.TextField()

    class Meta:
        verbose_name = "comment"
        verbose_name_plural = "comments"
        db_table = "tb_comment"


class ScheduleToPost(models.Model):
    schedule = models.ForeignKey(calendar_models.Schedule, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
