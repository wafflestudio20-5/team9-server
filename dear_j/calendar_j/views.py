import copy
import datetime

from dj_rest_auth import jwt_auth
from django import http
from django import shortcuts
from django.db.models import query
from rest_framework import authentication
from rest_framework import exceptions
from rest_framework import generics
from rest_framework import permissions
from rest_framework import request as req
from rest_framework import response as resp
from rest_framework import status

from calendar_j import exceptions as calendar_exceptions
from calendar_j import models as calendar_models
from calendar_j import paginations as calendar_paginations
from calendar_j import permissions as calendar_permissions
from calendar_j import serializers as calendar_serializers
from calendar_j.services.attendance import attendance
from calendar_j.services.protection import protection as calendar_protection
from user import models as user_models
from utils import time as time_utils


class ScheduleListCreateView(generics.ListCreateAPIView):
    authentication_classes = [
        jwt_auth.JWTCookieAuthentication,
        authentication.SessionAuthentication,
    ]
    queryset = calendar_models.Schedule.objects.all()
    pagination_class = calendar_paginations.ScheduleListPagination
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = calendar_serializers.ScheduleSerializer

    def get_queryset(self) -> query.QuerySet:
        params = self.request.GET
        if not all(key in params.keys() for key in ("pk", "from", "to")):
            raise calendar_exceptions.GetScheduleListKeyException

        target_user_pk = params.get("pk")
        target_user = shortcuts.get_object_or_404(user_models.User, pk=target_user_pk)

        start_date = time_utils.normal_date_formatter.parse(params.get("from"))
        end_date = time_utils.normal_date_formatter.parse(params.get("to"))

        participants = calendar_models.Participant.objects.filter(
            participant__pk=target_user_pk, status=attendance.AttendanceStatus.PRESENCE
        ).values_list("participant_id")

        queryset: query.QuerySet = super().get_queryset()

        total_queryset = queryset.filter(query.Q(created_by__pk=target_user_pk) | query.Q(participants__pk__in=participants))
        date_filtered_queryset = total_queryset.filter(
            query.Q(start_at__range=(start_date, end_date)) | query.Q(end_at__range=(start_date, end_date))
        )

        permission_refined_queryset = date_filtered_queryset.filter(
            protection_level__lte=calendar_protection.ProtectionLevel.filter_user_schedule(self.request.user, target_user),
            is_opened=True,
        )
        return permission_refined_queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return resp.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ScheduleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [
        jwt_auth.JWTCookieAuthentication,
        authentication.SessionAuthentication,
    ]
    queryset = calendar_models.Schedule.objects.all()
    permission_classes = [calendar_permissions.IsScheduleCreaterOrReader]
    serializer_class = calendar_serializers.ScheduleSerializer

    def delete(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        try:
            schedule = calendar_models.Schedule.objects.get(pk=pk)
        except calendar_models.Schedule.DoesNotExist:
            return http.JsonResponse({"error": "schedule object does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        schedule.is_opened = False
        schedule.save()
        return http.JsonResponse({}, status=status.HTTP_204_NO_CONTENT)


class ScheduleAttendanceUpdateView(generics.UpdateAPIView):
    authentication_classes = [
        jwt_auth.JWTCookieAuthentication,
        authentication.SessionAuthentication,
    ]
    queryset = calendar_models.Participant.objects.all()
    permission_classes = [calendar_permissions.IsScheduleParticipant]
    serializer_class = calendar_serializers.ParticipantSerializer

    def get_object(self) -> calendar_models.Participant:
        pk = self.kwargs["pk"]
        schedule = calendar_models.Schedule.objects.get(pk=pk)
        return shortcuts.get_object_or_404(calendar_models.Participant, participant=self.request.user, schedule=schedule)


class ScheduleGroupRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [
        jwt_auth.JWTCookieAuthentication,
        authentication.SessionAuthentication,
    ]
    queryset = calendar_models.ScheduleGroup.objects.all()
    permission_classes = [calendar_permissions.IsScheduleGroupCreator]
    serializer_class = calendar_serializers.ScheduleGroupSerializer

    def update(self, request: req.Request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        params = request.data

        schedules = calendar_models.Schedule.objects.filter(schedule_groups__id=self.kwargs["pk"])
        for schedule in schedules:
            updated_params = copy.deepcopy(params)
            if "cron_expr" in params.keys():
                raise exceptions.ValidationError("Recurring Rule cannot be updated")

            if ("start_at" in params.keys()) ^ ("end_at" in params.keys()):
                raise exceptions.ValidationError("start_at, end_at must be existed together")

            if all(key in params.keys() for key in ("start_at", "end_at")):
                start_at = time_utils.normal_datetime_formatter.parse(params.get("start_at"))
                end_at = time_utils.normal_datetime_formatter.parse(params.get("end_at"))

                updated_start_at = time_utils.replace_time(schedule.start_at, start_at)
                updated_end_at = time_utils.replace_time(schedule.end_at, end_at)
                updated_params.update(
                    {
                        "start_at": updated_start_at,
                        "end_at": updated_end_at,
                    }
                )

            schedule_serializer = calendar_serializers.ScheduleSerializer(instance=schedule, data=updated_params, partial=partial)
            schedule_serializer.is_valid(raise_exception=True)
            schedule_serializer.save()

            if getattr(schedule, "_prefetched_objects_cache", None):
                schedule._prefetched_objects_cache = {}

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return resp.Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        schedules = calendar_models.Schedule.objects.filter(schedule_groups__id=self.kwargs["pk"])
        for schedule in schedules:
            schedule.delete()

        instance = self.get_object()
        self.perform_destroy(instance)
        return resp.Response(status=status.HTTP_204_NO_CONTENT)
