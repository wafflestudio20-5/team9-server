from dj_rest_auth import views as dj_auth_views
from dj_rest_auth.registration import views as dj_reg_views
from rest_framework import response as rest_response
from rest_framework import status

from user import models
from user import permissions
from user import serializers


class UserRegistrationView(dj_reg_views.RegisterView):
    serializer_class = serializers.RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        birthdate = request.data.get("birthdate", "")

        user.birthdate = birthdate
        user.save()

        headers = self.get_success_headers(serializer.data)
        data = self.get_response_data(user)

        if data:
            response = rest_response.Response(
                data,
                status=status.HTTP_201_CREATED,
                headers=headers,
            )
        else:
            response = rest_response.Response(status=status.HTTP_204_NO_CONTENT, headers=headers)

        return response


class UserLoginView(dj_auth_views.LoginView):
    pass


class UserLogoutView(dj_auth_views.LogoutView):
    pass


class UserPasswordChangeView(dj_auth_views.PasswordChangeView):
    pass


class UserProfileView(dj_auth_views.UserDetailsView):
    serializer_class = serializers.UserDetailSerializer
    permission_classes = (permissions.UserIdentification,)

    def get_object(self) -> models.User:
        return self.request.user
