from rest_framework import permissions
from rest_framework import request as req

from calendar_j import models as calendar_models


class IsScheduleCreator(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request: req.HttpRequest, view, obj: calendar_models.Schedule) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.created_by == request.user


class IsScheduleParticipant(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request: req.HttpRequest, view, obj: calendar_models.Schedule) -> bool:
        if obj.participants.filter(pk=request.user.pk).first() is not None:
            return True
        return False
