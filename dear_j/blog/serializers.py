from typing import Dict

from django import shortcuts
from rest_framework import serializers

from blog import models as blog_models
from calendar_j import models as calendar_models
from calendar_j import serializers as calendar_serializers


class PostSerializer(serializers.ModelSerializer):
    schedules = calendar_serializers.ScheduleSerializer(read_only=True, many=True, required=False)

    class Meta:
        model = blog_models.Post
        fields = "__all__"
        extra_kwargs = {
            "created_by": {
                "default": serializers.CurrentUserDefault(),
            },
        }

    def create(self, validated_data: Dict) -> blog_models.Post:
        schedules_raw_data = self.initial_data.pop("schedules", [])
        schedule_ids = [row.get("pk") for row in schedules_raw_data]

        post: blog_models.Post = super().create(validated_data)

        for schedule_id in schedule_ids:
            schedule = shortcuts.get_object_or_404(calendar_models.Schedule, id=schedule_id)
            blog_models.ScheduleToPost.objects.create(post=post, schedule=schedule)

        post.save()
        return post

    def update(self, instance, validated_data: Dict) -> blog_models.Post:
        schedules_raw_data = self.initial_data.pop("schedules", [])
        schedule_ids = [row.get("pk") for row in schedules_raw_data]

        if schedules_raw_data is not []:
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
