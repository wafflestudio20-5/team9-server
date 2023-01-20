from django import urls

from user.views import common
from user.views.social_login import google
from user.views.social_login import kakao

urlpatterns = [
    # Common
    urls.path("registration/", common.UserRegistrationView.as_view()),
    urls.path("login/", common.UserLoginView.as_view()),
    urls.path("logout/", common.UserLogoutView.as_view()),
    urls.path("profile/", common.UserProfileView.as_view()),
    # # Kakao Social Login
    # urls.path("login/kakao/", kakao.KakaoView.as_view()),
    # urls.path("login/kakao/callback/", kakao.KakaoCallBackView.as_view()),
    # urls.path("login/kakao/finish/", kakao.KakaoLoginView.as_view()),
    # # Google Social Login
    # urls.path("login/google/", google.GoogleView.as_view()),
    # urls.path("login/google/callback/", google.GoogleCallBackView.as_view()),
    # urls.path("login/google/finish/", google.GoogleLoginView.as_view()),
]
