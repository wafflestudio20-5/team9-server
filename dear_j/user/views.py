from dj_rest_auth import views as dj_auth_views
from dj_rest_auth.registration import views as dj_reg_views


class UserRegistrationView(dj_reg_views.RegisterView):
    pass


class UserLoginView(dj_auth_views.LoginView):
    pass


class UserLogoutView(dj_auth_views.LogoutView):
    pass
