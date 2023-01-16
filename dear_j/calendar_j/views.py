from dj_rest_auth import jwt_auth
from django import http
from django.db.models import query
from rest_framework import authentication
from rest_framework import generics
from rest_framework import status

from calendar_j import exceptions as calendar_exceptions
from calendar_j import models as calendar_models
from calendar_j import paginations as calendar_paginations
from calendar_j import permissions as calendar_permissions
from calendar_j import serializers as calendar_serializers
from calendar_j.services.attendance import attendance
from calendar_j.services.protection import protection as calendar_protection
from utils import time as time_utils


class ScheduleListCreateView(generics.ListCreateAPIView):
    authentication_classes = [
        jwt_auth.JWTCookieAuthentication,
        authentication.SessionAuthentication,
    ]
    queryset = calendar_models.Schedule.objects.all()
    pagination_class = calendar_paginations.ScheduleListPagination
    permission_classes = [calendar_permissions.IsScheduleReader]
    serializer_class = calendar_serializers.ScheduleSerializer

    def get_queryset(self) -> query.QuerySet:
        params = self.request.GET
        if not all(key in params.keys() for key in ("pk", "from", "to")):
            raise calendar_exceptions.GetScheduleListKeyException

        target_pk = params.get("pk")
        start_date = time_utils.normal_date_formatter.parse(params.get("from"))
        end_date = time_utils.normal_date_formatter.parse(params.get("to"))

        queryset: query.QuerySet = super().get_queryset()

        created_queryset = queryset.filter(created_by__email=target_pk, start_at__range=(start_date, end_date)) | queryset.filter(
            created_by__email=target_pk, end_at__range=(start_date, end_date)
        )
        participant = calendar_models.Participant.objects.filter(
            participant__pk=target_pk, status=attendance.AttendanceStatus.PRESENCE
        ).values_list("participant_id")
        parcipating_queryset = queryset.filter(participants__pk__in=participant, start_at__range=(start_date, end_date)) | queryset.filter(
            participants__pk__in=participant, end_at__range=(start_date, end_date)
        )
        total_queryset = created_queryset | parcipating_queryset
        permission_refined_queryset = total_queryset.filter(
            protection_level__lte=calendar_protection.ProtectionLevel.filter_user_schedule(self.request.user, target_pk), is_opened=True
        )
        return permission_refined_queryset


class ScheduleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [
        jwt_auth.JWTCookieAuthentication,
        authentication.SessionAuthentication,
    ]
    queryset = calendar_models.Schedule.objects.all()
    permission_classes = [calendar_permissions.IsScheduleReader]
    serializer_class = calendar_serializers.ScheduleSerializer

    def delete(self, request, *args, **kwargs):
        try:
            pk = self.kwargs["pk"]
            schedule = calendar_models.Schedule.objects.get(pk=pk)
            schedule.is_opened = False
            schedule.save()
            output = http.JsonResponse({}, status=status.HTTP_204_NO_CONTENT)
        except calendar_models.Schedule.DoesNotExist:
            output = http.JsonResponse({"error": "schedule object does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        return output


class ScheduleAttendenceResponseView(generics.UpdateAPIView):
    authentication_classes = [
        jwt_auth.JWTCookieAuthentication,
        authentication.SessionAuthentication,
    ]
    queryset = calendar_models.Participant.objects.all()
    permission_classes = [calendar_permissions.IsScheduleParticipant]
    serializer_class = calendar_serializers.ParticipantSerializer

    def get_queryset(self) -> query.QuerySet:
        pk = self.kwargs["pk"]
        schedule = calendar_models.Schedule.objects.get(pk=pk)

        queryset: query.QuerySet = super().get_queryset()
        refined_queryset = queryset.filter(participant=self.request.user, schedule=schedule)
        return refined_queryset
