from dj_rest_auth import views as dj_auth_views
from dj_rest_auth.registration import views as dj_reg_views
from rest_framework import generics
from rest_framework import permissions

from user import models
from user import serializers


class UserRegistrationView(dj_reg_views.RegisterView):
    pass


class UserLoginView(dj_auth_views.LoginView):
    pass


class UserLogoutView(dj_auth_views.LogoutView):
    pass


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.UserDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self) -> models.User:
        return self.request.user
