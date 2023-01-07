from django import urls

from dj_rest_auth import views as dj_auth_views
from dj_rest_auth.registration import views as dj_regi_views

from user import views

urlpatterns = [
    urls.path("registration/", dj_regi_views.RegisterView.as_view()),
    urls.path("login/", dj_auth_views.LoginView.as_view()),
    urls.path("login/kakao/", views.KakaoView.as_view()),
    urls.path("login/kakao/callback/", views.KakaoCallBackView.as_view()),
    urls.path("login/kakao/finish/", views.KakaoLogin.as_view()),
    urls.path("login/google/", views.GoogleView.as_view()),
    urls.path("login/google/callback/", views.GoogleCallBackView.as_view()),
    urls.path("login/google/finish/", views.GoogleLogin.as_view()),
    urls.path("logout/", dj_auth_views.LogoutView.as_view()),
    urls.path("", urls.include("allauth.urls")),
    urls.path("profile/", views.UserProfileView.as_view()),
]
