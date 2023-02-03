import abc
from typing import Dict

from allauth.socialaccount import models as allauth_models
from allauth.socialaccount.providers.oauth2 import client
from allauth.socialaccount.providers.oauth2 import views as oauth2_views
from dj_rest_auth.registration import views as dj_reg_views
from django import shortcuts
from rest_framework import request as req
from rest_framework import response as resp
from rest_framework import views

from user import models
from user import serializers
from user.service.social_login.contexts import base
from user.service.social_login.models import messages


class SocialPlatformView(views.APIView, base.SocialPlatformContextMixin, abc.ABC):
    def get(self, _: req.HttpRequest) -> resp.Response:
        return shortcuts.redirect(self.authorize_uri)


class SocialPlatformLoginView(dj_reg_views.SocialLoginView, base.SocialPlatformContextMixin, abc.ABC):
    adapter_class = oauth2_views.OAuth2Adapter
    client_class = client.OAuth2Client
    format_kwarg = None


class SocialPlatformCallBackView(
    views.APIView,
    base.SocialPlatformContextMixin,
    messages.SocialLoginExceptionMessageMixin,
    abc.ABC,
):
    social_login_view: SocialPlatformLoginView = None

    def get(self, request: req.HttpRequest):
        code = request.GET.get("code")
        # Step I. Get access token for accessing user info from social platform
        token = self._get_access_token(code)
        if token.keys().__contains__("error"):
            return self._redirect_to_front_for_exception(self.invalid_token)
        access_token = token.get("access_token")

        # Step II. Sign In
        response = self._login(access_token, code)
        response.data.pop("user")
        return shortcuts.redirect(self.get_redirect_to_front(**response.data))

    @abc.abstractmethod
    def _get_access_token(self, code: str) -> Dict:
        raise NotImplementedError

    def _login(self, access_token: str, code: str) -> resp.Response:
        self.social_login_view.request = self.request
        self.social_login_view.serializer = serializers.SocialLoginSerializer(
            data={"access_token": access_token, "code": code},
            context={
                "request": self.social_login_view.request,
                "view": self.social_login_view,
            },
        )

        self.social_login_view.serializer.is_valid(raise_exception=True)
        user = self.social_login_view.serializer.validated_data["user"]

        if models.User.objects.filter(email=user.email) and not allauth_models.SocialAccount.objects.filter(
            email=user.email, provider=self.platform
        ):
            return self._redirect_to_front_for_exception(self.invalid_social_user)

        self.social_login_view.login()
        return self.social_login_view.get_response()

    def _redirect_to_front_for_exception(self, error_message: str):
        return shortcuts.redirect(self.get_redirect_to_front(error=error_message))
