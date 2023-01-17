import abc
from typing import Dict

import requests

from allauth.socialaccount import models as allauth_models
from allauth.socialaccount.providers.oauth2 import client
from allauth.socialaccount.providers.oauth2 import views as oauth2_views
from dj_rest_auth.registration import views as dj_reg_views
from django import shortcuts
from rest_framework import request as req
from rest_framework import response as resp
from rest_framework import status
from rest_framework import views

from user import models
from user.service.social_login import messages
from user.service.social_login.contexts import base


class SocialPlatformView(views.APIView, base.SocialPlatformContextMixin):
    def get(self, _: req.HttpRequest) -> resp.Response:
        return shortcuts.redirect(self.authorize_uri)


class SocialPlatformCallBackView(
    views.APIView,
    base.SocialPlatformContextMixin,
    messages.SocialLoginExceptionMessageMixin,
    abc.ABC,
):
    def get(self, request: req.HttpRequest):
        code = request.GET.get("code")

        # Step I. Get access token for accessing user info from social platform
        token = self._get_access_token(code)
        if token.keys().__contains__("error"):
            return self._redirect_to_front_for_exception(self.invalid_token)
        access_token = token.get("access_token")

        # Step II. Get user info from social platform
        user_info = self._get_user_raw_info(access_token)
        if user_info.keys().__contains__("error"):
            return self._redirect_to_front_for_exception(self.invalid_access_token)
        user_profile = self._get_user_profile(user_info)

        # Step III. Only for existing user
        is_new_user = not models.User.objects.filter(email=user_profile.get("email"))
        if not is_new_user:
            user = models.User.objects.get(email=user_profile.get("email"))
            if not self._is_valid_user_type(user):
                return self._redirect_to_front_for_exception(self.invalid_social_user)

        # Step IV. Sign In
        response = self._login(access_token, code)
        if response.status_code != status.HTTP_200_OK:
            return self._redirect_to_front_for_exception(self.fail_to_login)

        # Step V. Only for new user
        if is_new_user:
            self._update_user_info(user_profile)
        return shortcuts.redirect(self.get_redirect_to_front(**response.json()))

    def _get_access_token(self, code: str) -> Dict:
        return requests.get(self.get_token_uri(code)).json()

    @abc.abstractmethod
    def _get_user_raw_info(self, access_token: str) -> Dict:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_user_profile(self, user_raw_info: Dict) -> Dict:
        raise NotImplementedError

    @abc.abstractmethod
    def _update_user_info(self, user_profile):
        raise NotImplementedError

    def _login(self, access_token: str, code: str) -> resp.Response:
        return requests.post(self.finish_url, data={"access_token": access_token, "code": code})

    def _is_valid_user_type(self, user: models.User) -> bool:
        return bool(
            allauth_models.SocialAccount.objects.filter(
                user=user,
                provider=self.platform,
            )
        )

    def _redirect_to_front_for_exception(self, error_message: str):
        return shortcuts.redirect(self.get_redirect_to_front(error=error_message))


class SocialPlatformLoginView(dj_reg_views.SocialLoginView, base.SocialPlatformContextMixin):
    adapter_class = oauth2_views.OAuth2Adapter
    client_class = client.OAuth2Client
