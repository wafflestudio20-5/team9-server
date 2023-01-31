from typing import Dict

import requests

from allauth.socialaccount.providers.kakao import views

from user.service.social_login.contexts import kakao
from user.views.social_login import base


class KakaoView(base.SocialPlatformView, kakao.KakaoContextMixin):
    pass


class KakaoLoginView(base.SocialPlatformLoginView, kakao.KakaoContextMixin):
    adapter_class = views.KakaoOAuth2Adapter


class KakaoCallBackView(base.SocialPlatformCallBackView, kakao.KakaoContextMixin):
    social_login_view = KakaoLoginView()

    def _get_access_token(self, code: str) -> Dict:
        headers = {"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"}
        return requests.post(self.get_token_uri(code), headers=headers).json()
