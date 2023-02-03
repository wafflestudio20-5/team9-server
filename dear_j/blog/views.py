from django import shortcuts
from django.db.models import query

from rest_framework import authentication
from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import request as req

from dj_rest_auth import jwt_auth

from blog import models as blog_models
from blog import paginations as blog_paginations
from blog import permissions as blog_permissions
from blog import serializers as blog_serializers
from calendar_j import models as calendar_models


class PostListCreateView(generics.ListCreateAPIView):
    authentication_classes = [
        jwt_auth.JWTCookieAuthentication,
        authentication.SessionAuthentication,
    ]
    pagination_class = blog_paginations.PostListPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = blog_models.Post.objects.all()
    serializer_class = blog_serializers.PostSerializer


class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [
        jwt_auth.JWTCookieAuthentication,
        authentication.SessionAuthentication,
    ]
    permission_classes = [blog_permissions.IsPostCreator]
    queryset = blog_models.Post.objects.all()
    serializer_class = blog_serializers.PostSerializer
    lookup_field = "pid"


class CommentListCreateView(generics.ListCreateAPIView):
    authentication_classes = [
        jwt_auth.JWTCookieAuthentication,
        authentication.SessionAuthentication,
    ]
    pagination_class = blog_paginations.CommentListPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = blog_models.Comment.objects.all()
    serializer_class = blog_serializers.CommentSerializer


class CommentUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [
        jwt_auth.JWTCookieAuthentication,
        authentication.SessionAuthentication,
    ]
    permission_classes = [blog_permissions.IsCommentCreator]
    queryset = blog_models.Comment.objects.all()
    serializer_class = blog_serializers.CommentSerializer
    lookup_field = "cid"


class PostListFilteredByScheduleView(generics.ListCreateAPIView):
    authentication_classes = [
        jwt_auth.JWTCookieAuthentication,
        authentication.SessionAuthentication,
    ]
    pagination_class = blog_paginations.PostListPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = blog_models.Post.objects.all()
    serializer_class = blog_serializers.PostSerializer

    def get_queryset(self) -> query.QuerySet:
        schedule_pk = self.kwargs["pk"]
        schedule = shortcuts.get_object_or_404(calendar_models.Schedule, pk=schedule_pk)

        queryset: query.QuerySet = super().get_queryset()
        return queryset.filter(schedules=schedule)
