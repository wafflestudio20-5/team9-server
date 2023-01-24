from typing import Dict

from rest_framework import serializers

from blog import models as blog_models


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = blog_models.Post
        fields = "__all__"
        extra_kwargs = {
            "created_by": {
                "default": serializers.CurrentUserDefault(),
            },
        }


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = blog_models.Comment
        fields = "__all__"
        extra_kwargs = {
            "created_by": {
                "default": serializers.CurrentUserDefault(),
            },
        }
