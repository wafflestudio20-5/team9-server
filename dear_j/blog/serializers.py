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

    def update(self, instance, validated_data):
        instance.is_updated = True
        instance.save()
        return super().update(instance, validated_data)
