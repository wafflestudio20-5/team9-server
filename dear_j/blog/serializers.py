from typing import Dict

from django import http
from django import shortcuts
from django.core import exceptions
from rest_framework import fields
from rest_framework import serializers

from blog import models as blog_models
from calendar_j import models as calendar_models
from calendar_j import serializers as calendar_serializers


class PostSerializer(serializers.ModelSerializer):
    schedules = calendar_serializers.ScheduleFromPKSerializer(read_only=True, many=True, required=False)
    schedules_json = serializers.JSONField(write_only=True, required=False)

    class Meta:
        model = blog_models.Post
        fields = "__all__"
        extra_kwargs = {
            "created_by": {
                "default": serializers.CurrentUserDefault(),
            },
        }

    def validate_nested_json(self, value):
        if not isinstance(value, list):
            raise exceptions.ValidationError("nested json expects a list")
        for item in value:
            serializer = calendar_serializers.ScheduleFromPKSerializer(data=item)
            serializer.is_valid(raise_exception=True)
        return value

    def create(self, validated_data: Dict) -> blog_models.Post:
        schedule_dicts = validated_data.pop("schedules_json", [])
        schedule_ids = [row.get("pk") for row in schedule_dicts]

        post = super().create(validated_data)

        for schedule_id in schedule_ids:
            schedule = shortcuts.get_object_or_404(calendar_models.Schedule, pk=schedule_id)
            blog_models.ScheduleToPost.objects.create(post=post, schedule=schedule)

        post.save()
        return post

    def update(self, instance: blog_models.Post, validated_data: Dict) -> blog_models.Post:
        edit_schedules = validated_data.keys().__contains__("schedules_json")
        if edit_schedules:
            schedule_dicts = validated_data.pop("schedules_json")
            schedule_ids = [row.get("pk") for row in schedule_dicts]

        post = super().update(instance, validated_data)

        if edit_schedules:
            schedule_to_posts = blog_models.ScheduleToPost.objects.filter(post=instance)
            schedule_to_posts.delete()

            for schedule_id in schedule_ids:
                schedule = shortcuts.get_object_or_404(calendar_models.Schedule, id=schedule_id)
                blog_models.ScheduleToPost.objects.create(post=post, schedule=schedule)

        return post


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = blog_models.Comment
        fields = "__all__"
        extra_kwargs = {
            "created_by": {
                "default": serializers.CurrentUserDefault(),
            },
        }

    def update(self, instance, validated_data: Dict) -> blog_models.Comment:
        instance.is_updated = True
        instance.save()
        return super().update(instance, validated_data)
