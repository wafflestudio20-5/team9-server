from rest_framework import permissions
from rest_framework import request

from blog import models as blog_models


class IsPostCreator(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(
        self, request: request.Request, view, object: blog_models.Post
    ):
        if request.method in permissions.SAFE_METHODS:
            return True
        return object.created_by == request.user


class IsCommentCreator(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(
        self, request: request.Request, view, object: blog_models.Comment
    ):
        if request.method in permissions.SAFE_METHODS:
            return True
        return object.created_by == request.user
