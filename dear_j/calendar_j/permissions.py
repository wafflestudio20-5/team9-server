from rest_framework import permissions
from rest_framework import request as req

from calendar_j import models as calendar_models
from calendar_j.services.protection import protection
from social import models as social_models
from user import models as user_models


class IsScheduleCreator(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request: req.HttpRequest, view, obj: calendar_models.Schedule) -> bool:
        if obj.created_by == request.user:
            return True
        if obj.protection_level == protection.ProtectionLevel.CLOSED:
            return False
        if request.method not in permissions.SAFE_METHODS:
            return False
        if obj.protection_level == protection.ProtectionLevel.FOLLOWER:
            if social_models.Network.objects.filter(follower=request.user, followee=obj.created_by).first() is not None:
                return True
            return False
        if obj.protection_level == protection.ProtectionLevel.OPEN:
            return True
        return False


class IsScheduleParticipant(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request: req.HttpRequest, view, obj: calendar_models.Schedule) -> bool:
        if obj.participant == request.user:
            return True
        return False
