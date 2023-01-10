from django import urls

from user import views

urlpatterns = [
    urls.path("registration/", views.UserRegistrationView.as_view()),
    urls.path("login/", views.UserLoginView.as_view()),
    urls.path("logout/", views.UserLogoutView.as_view()),
    urls.path("login/kakao/", views.KakaoView.as_view()),
    urls.path("login/kakao/callback/", views.KakaoCallBackView.as_view()),
    urls.path("login/kakao/finish/", views.KakaoLogin.as_view()),
    urls.path("login/google/", views.GoogleView.as_view()),
    urls.path("login/google/callback/", views.GoogleCallBackView.as_view()),
    urls.path("login/google/finish/", views.GoogleLogin.as_view()),
    urls.path("", urls.include("allauth.urls")),
    urls.path("profile/", views.UserProfileView.as_view()),
]
