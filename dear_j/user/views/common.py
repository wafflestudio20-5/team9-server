from dj_rest_auth import views as dj_auth_views
from dj_rest_auth.registration import views as dj_reg_views

from user import permissions
from user import serializers


class UserRegistrationView(dj_reg_views.RegisterView):
    pass


class UserLoginView(dj_auth_views.LoginView):
    pass


class UserLogoutView(dj_auth_views.LogoutView):
    pass


class UserPasswordChangeView(dj_auth_views.PasswordChangeView):
    pass


class UserProfileView(dj_auth_views.UserDetailsView):
    permission_classes = (permissions.UserIdentification,)
    serializer_class = serializers.UserDetailSerializer
