from rest_framework import generics

from calendar_j import models as calendar_models
from calendar_j import serializers as calendar_serializers


class ScheduleListCreateView(generics.ListCreateAPIView):
    queryset = calendar_models.Schedule.objects.all()
    serializer_class = calendar_serializers.ScheduleSerializer


class ScheduleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = calendar_models.Schedule.objects.all()
    serializer_class = calendar_serializers.ScheduleSerializer
