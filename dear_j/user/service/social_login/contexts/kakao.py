import os

from user.service.social_login.contexts import base
from user.service.social_login.models import platforms
from utils import uri as uri_utils


class KakaoContextMixin(base.SocialPlatformContextMixin):
    platform = platforms.SocialPlatform.KAKAO.value
    oauth_url: str = "https://kauth.kakao.com/oauth/"

    @property
    def authorize_uri(self):
        authorize_url = os.path.join(self.oauth_url, "authorize")
        extra_params = {
            "client_id": self.client_id,
            "redirect_uri": self.callback_url,
            "response_type": self.response_type,
        }
        return uri_utils.get_uri_with_extra_params(authorize_url, extra_params)

    def get_token_uri(self, code):
        token_url = os.path.join(self.oauth_url, "token")
        extra_params = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.client_pw,
            "code": code,
            "redirect_uri": self.callback_url,
        }
        return uri_utils.get_uri_with_extra_params(token_url, extra_params)
