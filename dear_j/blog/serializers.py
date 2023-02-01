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
    schedules = calendar_serializers.SchedulePKSerializer(many=True, required=False)
    nested_json = serializers.JSONField(write_only=True)

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
            exceptions.ValidationError("nested json expects a list")
        for item in value:
            serializer = calendar_serializers.SchedulePKSerializer(data=item)
            serializer.is_valid(raise_exception=True)
        return value

    def create(self, validated_data: Dict) -> blog_models.Post:
        schedule_ordered_dicts = validated_data.pop("nested_json")
        schedule_ids = []
        for ordered_dicts in schedule_ordered_dicts:
            dic = dict(ordered_dicts)
            schedule_ids.append(dic.get("pk"))

        post: blog_models.Post = super().create(validated_data)

        for schedule_id in schedule_ids:
            schedule = shortcuts.get_object_or_404(calendar_models.Schedule, pk=schedule_id)
            blog_models.ScheduleToPost.objects.create(post=post, schedule=schedule)

        post.save()
        return post

    def update(self, instance, validated_data: Dict) -> blog_models.Post:
        try:
            schedule_ordered_dicts = validated_data.pop("nested_json")
            schedule_ids = []
            for ordered_dicts in schedule_ordered_dicts:
                dic = dict(ordered_dicts)
                schedule_ids.append(dic.get("pk"))
        except KeyError as e:
            schedule_ids = []

        if schedule_ids:
            past_schedule = blog_models.ScheduleToPost.objects.filter(post=instance)
            past_schedule.delete()

            for schedule_id in schedule_ids:
                schedule = shortcuts.get_object_or_404(calendar_models.Schedule, id=schedule_id)
                blog_models.ScheduleToPost.objects.create(post=instance, schedule=schedule)

        instance.save()
        return super().update(instance, validated_data)


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


class ScheduleToPostSerializer(serializers.ModelSerializer):
    schedules = calendar_serializers.ScheduleSerializer(read_only=True, many=True, required=False)

    class Meta:
        model = blog_models.Post
        fields = "__all__"
        extra_kwargs = {
            "created_by": {
                "default": serializers.CurrentUserDefault(),
            },
        }
