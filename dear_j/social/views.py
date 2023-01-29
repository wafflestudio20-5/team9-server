from dj_rest_auth import jwt_auth
from django.db.models import query
from rest_framework import authentication
from rest_framework import filters
from rest_framework import generics

from social import models as social_models
from social import paginations as social_paginations
from social import permissions as social_permissions
from social import serializers as social_serializers
from user import models as user_models
from user import serializers as user_serializers


class FollowCandidateSearchListView(generics.ListAPIView):
    authentication_classes = [
        jwt_auth.JWTCookieAuthentication,
        authentication.SessionAuthentication,
    ]
    queryset = user_models.User.objects.all()
    pagination_class = social_paginations.CandidateListPagination
    serializer_class = user_serializers.EssentialUserInfoFromPKSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["username", "email"]


class NetworkFollowerListView(generics.ListAPIView):
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


class NetworkFollowerUpdateView(generics.UpdateAPIView):
    authentication_classes = [
        jwt_auth.JWTCookieAuthentication,
        authentication.SessionAuthentication,
    ]
    queryset = social_models.Network.objects.all()
    permission_classes = [social_permissions.IsNetworkFollowee]
    serializer_class = social_serializers.NetworkSerializer


class NetworkFolloweeListCreateView(generics.ListCreateAPIView):
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
    authentication_classes = [
        jwt_auth.JWTCookieAuthentication,
        authentication.SessionAuthentication,
    ]
    queryset = social_models.Network.objects.all()
    permission_classes = [social_permissions.IsNetworkFollower]
    serializer_class = social_serializers.NetworkSerializer
