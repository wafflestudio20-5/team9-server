from rest_framework import permissions
from rest_framework import request as req

from user import models as user_models


class UserIdentification(permissions.IsAuthenticated):
    def has_object_permission(self, request: req.HttpRequest, view, obj: user_models.User) -> bool:
        return obj == request.user
