from typing import Dict

import requests

from allauth.socialaccount.providers.kakao import views

from user.service.social_login.contexts import kakao
from user.views.social_login import base


class KakaoView(base.SocialPlatformView, kakao.KakaoContextMixin):
    pass


class KakaoCallBackView(base.SocialPlatformCallBackView, kakao.KakaoContextMixin):
    def _get_user_raw_info(self, access_token) -> Dict:
        return requests.get(
            url=self.profile_url,
            headers={"Authorization": f"Bearer {access_token}"},
        ).json()

    def _get_user_profile(self, user_raw_info: Dict) -> Dict:
        return user_raw_info.get("kakao_account")

    def _update_user_info(self, user_profile):
        raise NotImplementedError


class KakaoLoginView(base.SocialPlatformLoginView, kakao.KakaoContextMixin):
    adapter_class = views.KakaoOAuth2Adapter
