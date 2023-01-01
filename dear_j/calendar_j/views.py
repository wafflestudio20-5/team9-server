from rest_framework import generics

from calendar_j import models as calendar_models
from calendar_j import paginations as calendar_paginations
from calendar_j import permissions as calendar_permissions
from calendar_j import serializers as calendar_serializers


class ScheduleListCreateView(generics.ListCreateAPIView):
    queryset = calendar_models.Schedule.objects.all()
    pagination_class = calendar_paginations.ScheduleListPagination
    permission_classes = [calendar_permissions.IsScheduleCreator]
    serializer_class = calendar_serializers.ScheduleSerializer


class ScheduleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = calendar_models.Schedule.objects.all()
    permission_classes = [calendar_permissions.IsScheduleCreator]
    serializer_class = calendar_serializers.ScheduleSerializer
