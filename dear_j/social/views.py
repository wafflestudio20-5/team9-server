from dj_rest_auth import jwt_auth
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
    serializer_class = user_serializers.UserEmailSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["email", "username"]


class NetworkListCreateView(generics.ListCreateAPIView):
    # TODO: User can only access to related network
    authentication_classes = [
        jwt_auth.JWTCookieAuthentication,
        authentication.SessionAuthentication,
    ]
    queryset = social_models.Network.objects.all()
    pagination_class = social_paginations.NetworkListPagination
    permission_classes = [social_permissions.NetworkPermission]
    serializer_class = social_serializers.NetworkSerializer


class NetworkRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    # TODO: Change approved state from "False" to "True" must only be allowed to followee
    # TODO: Change is_opened state must only be allowed to follower
    authentication_classes = [
        jwt_auth.JWTCookieAuthentication,
        authentication.SessionAuthentication,
    ]
    queryset = social_models.Network.objects.all()
    permission_classes = [social_permissions.NetworkPermission]
    serializer_class = social_serializers.NetworkSerializer
