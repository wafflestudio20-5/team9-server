import abc
from typing import Dict

from allauth.socialaccount import models as allauth_models
from allauth.socialaccount.providers.google import views as google_view
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.oauth2 import client
from dj_rest_auth import views as dj_auth_views
from dj_rest_auth.registration import views as dj_reg_views
from django import shortcuts
from rest_framework import generics
from rest_framework import permissions
from rest_framework import request as req
from rest_framework import response as resp
from rest_framework import status
from rest_framework import views

import requests
from user import models
from user import serializers
from user.service.social_login import platforms


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


class SocialPlatformCallBackView(views.APIView, platforms.SocialPlatformContextMixin, abc.ABC):
    def get(self, request: req.HttpRequest):
        code = request.GET.get("code")

        access_token = self._get_access_token(code)
        user_info = self._get_user_info(access_token)

        user = self._get_user(user_info.get("email"), access_token, code)
        if self._is_valid_user_type(user):
            return self._redirect_to_front_for_exception("Invalid Kakao Login")

        accept = self._sign_up(access_token, code)
        return shortcuts.redirect(self.get_redirect_to_front(**accept))

    def _get_access_token(self, code):
        token: Dict = requests.get(self.get_token_uri(code)).json()
        if token.keys().__contains__("error"):
            return self._redirect_to_front_for_exception("invalid-KAKAO-token")
        return token.get("access_token")

    @abc.abstractmethod
    def _get_user_info(self, access_token) -> Dict:
        raise NotImplementedError

    def _get_user(self, email: str, access_token: str, code: str) -> models.User:
        if not models.User.objects.filter(email=email):
            response = requests.post(
                self.finish_url,
                data={
                    "access_token": access_token,
                    "code": code,
                },
            )

            if response.status_code != status.HTTP_200_OK:
                return self._redirect_to_front_for_exception("failed-to-register")
        return models.User.objects.get(email=email)

    def _is_valid_user_type(self, user: models.User) -> bool:
        return bool(
            allauth_models.SocialAccount.objects.filter(
                user=user,
                provider=self.platform,
            )
        )

    def _sign_up(self, access_token: str, code: str) -> Dict:
        response = requests.post(
            self.finish_url,
            data={
                "access_token": access_token,
                "code": code,
            },
        )
        if response.status_code != status.HTTP_200_OK:
            return self._redirect_to_front_for_exception("failed-to-sign-in")
        return response.json()

    def _redirect_to_front_for_exception(self, error_message: str):
        return shortcuts.redirect(self.get_redirect_to_front(error=error_message))


class KakaoView(views.APIView, platforms.KakaoContextMixin):
    def get(self, _: req.HttpRequest) -> resp.Response:
        return shortcuts.redirect(self.authorize_uri)


class KakaoCallBackView(SocialPlatformCallBackView, platforms.KakaoContextMixin):
    def _get_user_info(self, access_token) -> Dict:
        profile_json: Dict = requests.get(
            url=self.profile_url,
            headers={"Authorization": f"Bearer {access_token}"},
        ).json()

        if profile_json.keys().__contains__("error"):
            return self._redirect_to_front_for_exception("invalid-profile-request-token")
        return profile_json.get("kakao_account")


class KakaoLogin(dj_reg_views.SocialLoginView, platforms.KakaoContextMixin):
    adapter_class = kakao_view.KakaoOAuth2Adapter
    client_class = client.OAuth2Client


class GoogleView(views.APIView, platforms.GoogleContextMixin):
    def get(self, _: req.HttpRequest) -> resp.Response:
        return shortcuts.redirect(self.authorize_uri)


class GoogleCallBackView(SocialPlatformCallBackView, platforms.GoogleContextMixin):
    def _get_user_info(self, access_token) -> Dict:
        profile_json: Dict = requests.get(self.get_email_uri(access_token)).json()

        if profile_json.keys().__contains__("error"):
            return self._redirect_to_front_for_exception("invalid-profile-request-token")
        return profile_json


class GoogleLogin(dj_reg_views.SocialLoginView, platforms.GoogleContextMixin):
    adapter_class = google_view.GoogleOAuth2Adapter
    client_class = client.OAuth2Client
