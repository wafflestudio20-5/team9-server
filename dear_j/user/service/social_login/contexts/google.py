import os

from user.service.social_login.contexts import base
from user.service.social_login.models import platforms
from utils import uri as uri_utils


class GoogleContextMixin(base.SocialPlatformContextMixin):
    platform = platforms.SocialPlatform.GOOGLE.value
    account_url: str = "https://accounts.google.com/"
    personal_api_url: str = "https://people.googleapis.com/v1/people/me"

    @property
    def authorize_uri(self) -> str:
        authorize_url = os.path.join(self.account_url, "o/oauth2/v2/auth")
        extra_params = {
            "client_id": self.client_id,
            "redirect_uri": self.callback_url,
            "response_type": self.response_type,
            "scope": (
                "https://www.googleapis.com/auth/user.birthday.read "
                "https://www.googleapis.com/auth/userinfo.email "
                "https://www.googleapis.com/auth/userinfo.profile"
            ),
        }
        return uri_utils.get_uri_with_extra_params(authorize_url, extra_params)

    def get_token_uri(self, code: str) -> str:
        token_url = os.path.join("https://oauth2.googleapis.com/", "token")
        extra_params = {
            "grant_type": "authorization_code",
            "state": "state",
            "client_id": self.client_id,
            "client_secret": self.client_pw,
            "redirect_uri": self.callback_url,
            "code": code,
        }
        return uri_utils.get_uri_with_extra_params(token_url, extra_params)

    def get_email_uri(self, access_token: str):
        email_url = os.path.join(self.account_url, "oauth2/v1/tokeninfo")
        return uri_utils.get_uri_with_extra_params(email_url, {"access_token": access_token})

    def get_personal_api_uri(self, field: str):
        return uri_utils.get_uri_with_extra_params(self.personal_api_url, {"personFields": field})
