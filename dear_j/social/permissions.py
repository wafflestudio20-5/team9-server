from rest_framework import permissions
from rest_framework import request as req

from social import models as social_models


class NetworkPermission(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request: req.HttpRequest, view, obj: social_models.Network) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user in (obj.follower, obj.followee)
