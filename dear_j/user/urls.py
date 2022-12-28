from django import urls

from dj_rest_auth import views as dj_auth_views
from dj_rest_auth.registration import views as dj_regi_views

urlpatterns = [
    urls.path("registration/", dj_regi_views.RegisterView.as_view()),
    urls.path("login/", dj_auth_views.LoginView.as_view()),
    urls.path("logout/", dj_auth_views.LogoutView.as_view()),
]
