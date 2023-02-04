from dj_rest_auth import jwt_auth
from django.db.models import query
from rest_framework import authentication
from rest_framework import filters
from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions

from social import models as social_models
from social import paginations as social_paginations
from social import permissions as social_permissions
from social import serializers as social_serializers
from user import models as user_models
from user import serializers as user_serializers


class FollowCandidateSearchListView(generics.ListAPIView):
    """Search User."""

    authentication_classes = [
        jwt_auth.JWTCookieAuthentication,
        authentication.SessionAuthentication,
    ]
    queryset = user_models.User.objects.all()
    pagination_class = social_paginations.CandidateListPagination
    serializer_class = user_serializers.UserInfoSearchSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["username", "email"]


class NetworkFollowerListView(generics.ListAPIView):
    """Get All List of user who wants to follow request user."""

    authentication_classes = [
        jwt_auth.JWTCookieAuthentication,
        authentication.SessionAuthentication,
    ]
    queryset = social_models.Network.objects.all()
    pagination_class = social_paginations.NetworkListPagination
    permission_classes = [social_permissions.IsNetworkFollowee]
    serializer_class = social_serializers.NetworkSerializer

    def get_queryset(self) -> query.QuerySet:
        followee = self.request.user
        queryset: query.QuerySet = super().get_queryset()
        return queryset.filter(followee=followee)


class NetworkFollowerUpdateView(
    mixins.UpdateModelMixin,
    generics.GenericAPIView,
):
    """Accept or Reject follow request."""

    authentication_classes = [
        jwt_auth.JWTCookieAuthentication,
        authentication.SessionAuthentication,
    ]
    queryset = social_models.Network.objects.all()
    permission_classes = [social_permissions.IsNetworkFollowee]
    serializer_class = social_serializers.NetworkSerializer

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class NetworkFolloweeListCreateView(generics.ListCreateAPIView):
    """Request follow and Get All List of user that you request to follow."""

    authentication_classes = [
        jwt_auth.JWTCookieAuthentication,
        authentication.SessionAuthentication,
    ]
    queryset = social_models.Network.objects.all()
    pagination_class = social_paginations.NetworkListPagination
    permission_classes = [social_permissions.IsNetworkFollower]
    serializer_class = social_serializers.NetworkSerializer

    def get_queryset(self) -> query.QuerySet:
        follower = self.request.user
        queryset: query.QuerySet = super().get_queryset()
        return queryset.filter(follower=follower)


class NetworkFolloweeDestroyView(generics.DestroyAPIView):
    """Cancel follow request."""

    authentication_classes = [
        jwt_auth.JWTCookieAuthentication,
        authentication.SessionAuthentication,
    ]
    queryset = social_models.Network.objects.all()
    permission_classes = [social_permissions.IsNetworkFollower]
    serializer_class = social_serializers.NetworkSerializer


class NetworkNotificationView(generics.ListAPIView):
    authentication_classes = [
        jwt_auth.JWTCookieAuthentication,
        authentication.SessionAuthentication,
    ]
    queryset = social_models.Network.objects.all()
    pagination_class = social_paginations.NetworkListPagination
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = social_serializers.NetworkSerializer

    def get_queryset(self) -> query.QuerySet:
        followee = self.request.user
        queryset: query.QuerySet = super().get_queryset()
        return queryset.filter(followee=followee, approved=None)
