import abc
import os

from dear_j import settings
from user.service.social_login.models import platforms
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
