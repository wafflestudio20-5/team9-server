from typing import Dict

import requests

from allauth.socialaccount.providers.google import views

from user.service.social_login.contexts import google
from user.views.social_login import base


class GoogleView(base.SocialPlatformView, google.GoogleContextMixin):
    pass


class GoogleLoginView(base.SocialPlatformLoginView, google.GoogleContextMixin):
    adapter_class = views.GoogleOAuth2Adapter


class GoogleCallBackView(base.SocialPlatformCallBackView, google.GoogleContextMixin):
    social_login_view = GoogleLoginView()

    def _get_access_token(self, code: str) -> Dict:
        return requests.post(self.get_token_uri(code)).json()
