from django.db import models
from user import models as user_models


class Post(models.Model):
    pid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    created_by = models.ForeignKey(user_models.User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField()
    image = models.ImageField(upload_to="user", editable=True, null=True)

    class Meta:
        verbose_name = "post"
        verbose_name_plural = "posts"
        db_table = "tb_posts"

    def __str__(self):
        return str(self.title)


class Comment(models.Model):
    cid = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_by = models.ForeignKey(user_models.User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_updated = models.BooleanField(default=False)
    content = models.TextField()

    class Meta:
        verbose_name = "comment"
        verbose_name_plural = "comments"
        db_table = "tb_comments"
