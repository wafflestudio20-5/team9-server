import abc
import os

from dear_j import settings
from user.service.social_login import platforms
from utils import ssm as ssm_utils
from utils import uri as uri_utils


class SocialPlatformContextMixin(abc.ABC):
    platform: platforms.SocialPlatform
    oauth_url: str
    response_type: str = "code"

    @property
    def redirect_frontend_url(self):
        return os.path.join(settings.BASE_FE_URI, "login")

    @property
    def callback_url(self):
        return os.path.join(settings.BASE_BE_URI, f"api/v1/user/login/{self.platform}/callback/")

    @property
    def finish_url(self):
        return os.path.join(settings.BASE_BE_URI, f"api/v1/user/login/{self.platform}/finish/")

    @property
    def client_id(self):
        return ssm_utils.get_ssm_parameter(alias=f"/backend/dearj/{self.platform}/client-id")

    @property
    def client_pw(self):
        return ssm_utils.get_ssm_parameter(alias=f"/backend/dearj/{self.platform}/client-pw")

    def get_redirect_to_front(self, **kwargs):
        return uri_utils.get_uri_with_extra_params(self.redirect_frontend_url, kwargs)

    @property
    @abc.abstractmethod
    def authorize_uri(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_token_uri(self, code):
        raise NotImplementedError


class KakaoContextMixin(SocialPlatformContextMixin):
    platform = platforms.SocialPlatform.KAKAO.value
    oauth_url: str = "https://kauth.kakao.com/oauth/"
    profile_url: str = "https://kapi.kakao.com/v2/user/me"

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
            "redirect_uri": self.callback_url,
            "code": code,
        }
        return uri_utils.get_uri_with_extra_params(token_url, extra_params)


class GoogleContextMixin(SocialPlatformContextMixin):
    platform = platforms.SocialPlatform.GOOGLE.value
    oauth_url: str = "https://accounts.google.com/oauth2/"  # Question: 주소 확인

    @property
    def authorize_uri(self) -> str:
        authorize_url = os.path.join("https://accounts.google.com/o/oauth2/v2/auth", "v2/auth")
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
        token_url = os.path.join("https://oauth2.googleapis.com/token?", "token")
        extra_params = {
            "grant_type": "authorization_code",
            "state": "state",
            "client_id": self.client_id,
            "client_pw": self.client_pw,
            "redirect_uri": self.callback_url,
            "code": code,
        }
        return uri_utils.get_uri_with_extra_params(token_url, extra_params)

    def get_email_uri(self, access_token: str):
        email_url = os.path.join(self.oauth_url, "v1/tokeninfo")
        return uri_utils.get_uri_with_extra_params(email_url, {"access_token": access_token})
