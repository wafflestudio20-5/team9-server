from typing import Dict

from allauth.socialaccount.providers.google import views

import requests

from user.service.social_login.contexts import google
from user.views.social_login import base


class GoogleView(base.SocialPlatformView, google.GoogleContextMixin):
    pass


class GoogleCallBackView(base.SocialPlatformCallBackView, google.GoogleContextMixin):
    def _get_user_raw_info(self, access_token) -> Dict:
        return requests.get(self.get_email_uri(access_token)).json()

    def _get_user_profile(self, user_raw_info: Dict) -> Dict:
        return user_raw_info

    def _update_user_info(self, user_profile):
        raise NotImplementedError


class GoogleLoginView(base.SocialPlatformLoginView, google.GoogleContextMixin):
    adapter_class = views.GoogleOAuth2Adapter
