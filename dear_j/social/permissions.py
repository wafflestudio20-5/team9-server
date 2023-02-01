from rest_framework import permissions
from rest_framework import request as req

from social import models as social_models


class IsNetworkFollower(permissions.IsAuthenticated):
    def has_object_permission(self, request: req.HttpRequest, view, obj: social_models.Network) -> bool:
        return request.user == obj.follower


class IsNetworkFollowee(permissions.IsAuthenticated):
    def has_object_permission(self, request: req.HttpRequest, view, obj: social_models.Network) -> bool:
        return request.user == obj.followee
