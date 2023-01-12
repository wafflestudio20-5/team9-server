import json

from django import shortcuts
from rest_framework import generics
from rest_framework import permissions
from rest_framework import views as rest_views

from allauth.socialaccount import models as allauth_models
from allauth.socialaccount.providers.google import views as google_view
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.oauth2 import client
from dj_rest_auth import views as dj_auth_views
from dj_rest_auth.registration import views as dj_reg_views
import requests
import site_env
from user import models
from user import serializers
from user.service import common
from user.service import google
from user.service import kakao
from utils import ssm

if site_env.is_prod():
    BASE_BE_URI = "http://ec2-43-201-9-194.ap-northeast-2.compute.amazonaws.com/"
    BASE_FE_URI = "https://db5p3zym5dolm.cloudfront.net/"
else:
    BASE_BE_URI = "http://127.0.0.1:8000/"
    BASE_FE_URI = "http://127.0.0.1:3000/"

FE_LOGIN_URI = f"{BASE_FE_URI}login"
KAKAO_CLIENT_ID = ssm.get_ssm_parameter(alias="/backend/dearj/kakao/client-id")
KAKAO_CLIENT_PW = ssm.get_ssm_parameter(alias="/backend/dearj/kakao/client-pw")
KAKAO_REDIRECT_URI = f"{BASE_BE_URI}api/v1/user/login/kakao/callback/"
GOOGLE_CLIENT_ID = ssm.get_ssm_parameter(alias="/backend/dearj/google/client-id")
GOOGLE_CLIENT_PW = ssm.get_ssm_parameter(alias="/backend/dearj/google/client-pw")
GOOGLE_REDIRECT_URI = f"{BASE_BE_URI}api/v1/user/login/google/callback/"


class UserRegistrationView(dj_reg_views.RegisterView):
    pass


class UserLoginView(dj_auth_views.LoginView):
    pass


class UserLogoutView(dj_auth_views.LogoutView):
    pass


class KakaoView(rest_views.APIView):
    def get(self, request):
        return shortcuts.redirect(kakao.kauth_authorize_string(KAKAO_CLIENT_ID, KAKAO_REDIRECT_URI))


class KakaoCallBackView(rest_views.APIView):
    def get(self, request):
        birthday = "9999-12-31"
        try:
            # 1st request - get token
            code = request.GET.get("code")
            token_result = requests.get(kakao.kauth_token_string(KAKAO_CLIENT_ID, KAKAO_REDIRECT_URI, code))
            token_json = token_result.json()
            if common.token_error_occur(token_json):
                params = {"error": "invalid-KAKAO-token"}
                output = shortcuts.redirect(common.get_fe_redirect_url(FE_LOGIN_URI, params))
            # 2nd request - get user info
            access_token = token_json.get("access_token")
            profile_request = requests.get("https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {access_token}"})
            profile_json = profile_request.json()
            if common.token_error_occur(profile_json):
                params = {"error": "invalid-profile-request-token"}
                output = shortcuts.redirect(common.get_fe_redirect_url(FE_LOGIN_URI, params))
            email = kakao.get_email(profile_json)
            birthday = kakao.get_birthday(profile_json)
            username = kakao.get_username(profile_json)
            # check user type
            user = models.User.objects.get(email=email)
            social_user = allauth_models.SocialAccount.objects.get(user=user)
            if social_user is None:
                params = {"error": "Email-exists-but-not-social-user"}
                output = shortcuts.redirect(common.get_fe_redirect_url(FE_LOGIN_URI, params))
            if social_user.provider != "kakao":
                params = {"error": "Email-exists-but-not-kakao-user"}
                output = shortcuts.redirect(common.get_fe_redirect_url(FE_LOGIN_URI, params))
            # finish login - jwt token
            accept = requests.post(f"{BASE_BE_URI}api/v1/user/login/kakao/finish/", data={"access_token": access_token, "code": code})
            # redirect to frontend
            accept_status = accept.status_code
            if accept_status != 200:
                params = {"error": "failed-to-signin"}
                output = shortcuts.redirect(common.get_fe_redirect_url(FE_LOGIN_URI, params))
            accept_json = accept.json()
            accept_json.pop("user", None)
            output = shortcuts.redirect(common.get_fe_redirect_url(FE_LOGIN_URI, accept_json))

        except models.User.DoesNotExist:
            # register
            accept = requests.post(f"{BASE_BE_URI}api/v1/user/login/kakao/finish/", data={"access_token": access_token, "code": code})
            accept_status = accept.status_code
            if accept_status != 200:
                params = {"error": "failed-to-register"}
                output = shortcuts.redirect(common.get_fe_redirect_url(FE_LOGIN_URI, params))
            # redirect to front end
            accept_json = accept.json()
            accept_json.pop("user", None)
            new_user = models.User.objects.get(email=email)
            if birthday != "9999-12-31":
                new_user.birthdate = birthday
                new_user.save()
            output = shortcuts.redirect(common.get_fe_redirect_url(FE_LOGIN_URI, accept_json))
        return output


class KakaoLogin(dj_reg_views.SocialLoginView):
    adapter_class = kakao_view.KakaoOAuth2Adapter
    client_class = client.OAuth2Client
    callback_url = KAKAO_REDIRECT_URI


class GoogleView(rest_views.APIView):
    def get(self, request):
        return shortcuts.redirect(google.google_oauth_string(GOOGLE_CLIENT_ID, GOOGLE_REDIRECT_URI))


class GoogleCallBackView(rest_views.APIView):
    def get(self, request):
        # access token request
        code = request.GET.get("code")
        token_request = requests.post(google.google_token_string(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_PW, GOOGLE_REDIRECT_URI, code))
        token_req_json = token_request.json()
        if common.token_error_occur(token_req_json):
            params = {"error": "invalid-google-token"}
            return shortcuts.redirect(common.get_fe_redirect_url(FE_LOGIN_URI, params))
        access_token = token_req_json.get("access_token")
        # request email
        email_req = requests.get(google.google_email_request(access_token))
        if common.response_error_occur(email_req):
            params = {"error": "failed-to-get-email"}
            return shortcuts.redirect(common.get_fe_redirect_url(FE_LOGIN_URI, params))
        email = google.get_email(email_req)
        # request birthday
        birthday_req = requests.get(
            "https://people.googleapis.com/v1/people/me?personFields=birthdays", headers={"Authorization": f"Bearer {access_token}"}
        )
        birthday = google.get_birthday(birthday_req)
        try:
            # check user type
            user_type = google.check_user_type(email)
            if user_type == "general_user":
                params = {"error": "email-exists-but-not-social-user"}
                output = shortcuts.redirect(common.get_fe_redirect_url(FE_LOGIN_URI, params))
            elif user_type == "kakao_user":
                params = {"error": "no-matching-social-type"}
                output = shortcuts.redirect(common.get_fe_redirect_url(FE_LOGIN_URI, params))
            # google account exist -> sign in
            accept = requests.post(f"{BASE_BE_URI}api/v1/user/login/google/finish/", data={"access_token": access_token, "code": code})
            if common.response_error_occur(accept):
                params = {"error": "failed-to-signin"}
                output = shortcuts.redirect(common.get_fe_redirect_url(FE_LOGIN_URI, params))
            accept_json = accept.json()
            accept_json.pop("user", None)
            output = shortcuts.redirect(common.get_fe_redirect_url(FE_LOGIN_URI, accept_json))
        except models.User.DoesNotExist:
            # register user
            accept = requests.post(f"{BASE_BE_URI}api/v1/user/login/google/finish/", data={"access_token": access_token, "code": code})
            if common.response_error_occur(accept):
                params = {"error": "failed-to-signup"}
                output = shortcuts.redirect(common.get_fe_redirect_url(FE_LOGIN_URI, params))
            user = models.User.objects.get(email=email)
            if birthday != "9999-12-31":
                user.birthdate = birthday
                user.save()
            accept_json = accept.json()
            accept_json.pop("user", None)
            output = shortcuts.redirect(common.get_fe_redirect_url(FE_LOGIN_URI, accept_json))
        return output


class GoogleLogin(dj_reg_views.SocialLoginView):
    adapter_class = google_view.GoogleOAuth2Adapter
    callback_url = GOOGLE_REDIRECT_URI
    client_class = client.OAuth2Client


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.UserDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user
