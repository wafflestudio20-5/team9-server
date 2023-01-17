from dj_rest_auth import views as dj_auth_views
from dj_rest_auth.registration import views as dj_reg_views
from rest_framework import generics
from rest_framework import permissions
from rest_framework import response
from rest_framework import status

from user import serializers

from .models import User


class UserRegistrationView(dj_reg_views.RegisterView):
    pass


class UserLoginView(dj_auth_views.LoginView):
    pass


class UserLogoutView(dj_auth_views.LogoutView):
    pass


class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user
