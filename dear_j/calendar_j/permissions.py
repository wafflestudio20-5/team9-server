from rest_framework import permissions
from rest_framework import request as req

from calendar_j import models as calendar_models
from calendar_j.services.protection import protection


class IsScheduleCreatorOrReader(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request: req.HttpRequest, view, obj: calendar_models.Schedule) -> bool:
        if obj.created_by == request.user:
            return True
        if request.method not in permissions.SAFE_METHODS:
            return False
        return protection.ProtectionLevel.allow_request_user(obj.protection_level, request.user, obj.created_by)


class IsScheduleParticipant(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request: req.HttpRequest, view, obj: calendar_models.Participant) -> bool:
        return obj.participant == request.user


class IsRecurringScheduleGroupCreator(permissions.IsAuthenticated):
    def has_object_permission(self, request: req.HttpRequest, view, obj: calendar_models.RecurringScheduleGroup) -> bool:
        return obj.created_by == request.user
