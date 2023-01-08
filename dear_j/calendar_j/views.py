from dj_rest_auth import jwt_auth
from django.db.models import query
from rest_framework import authentication
from rest_framework import generics

from calendar_j import exceptions as calendar_exceptions
from calendar_j import models as calendar_models
from calendar_j import paginations as calendar_paginations
from calendar_j import permissions as calendar_permissions
from calendar_j import serializers as calendar_serializers
from utils import time as time_utils


class ScheduleListCreateView(generics.ListCreateAPIView):
    authentication_classes = [
        jwt_auth.JWTCookieAuthentication,
        authentication.SessionAuthentication,
    ]
    queryset = calendar_models.Schedule.objects.all()
    pagination_class = calendar_paginations.ScheduleListPagination
    permission_classes = [calendar_permissions.IsScheduleCreator]
    serializer_class = calendar_serializers.ScheduleSerializer

    def get_queryset(self) -> query.QuerySet:
        queryset: query.QuerySet = super().get_queryset()
        params = self.request.GET
        if not all(key in params.keys() for key in ("email", "from", "to")):
            raise calendar_exceptions.GetScheduleListKeyException

        target_email = params.get("email")
        start_date = time_utils.normal_date_formatter.parse(params.get("from"))
        end_date = time_utils.normal_date_formatter.parse(params.get("to"))

        refined_queryset = queryset.filter(created_by__email=target_email, start_at__range=(start_date, end_date)) | queryset.filter(
            participants__email=target_email, start_at__range=(start_date, end_date)
        )
        return refined_queryset


class ScheduleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [
        jwt_auth.JWTCookieAuthentication,
        authentication.SessionAuthentication,
    ]
    queryset = calendar_models.Schedule.objects.all()
    permission_classes = [calendar_permissions.IsScheduleCreator]
    serializer_class = calendar_serializers.ScheduleSerializer
