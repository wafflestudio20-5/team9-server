from typing import Dict

import requests

from allauth.socialaccount.providers.kakao import views

from user.service.social_login.contexts import kakao
from user.service.social_login.models import profile
from user.views.social_login import base
from utils import time as time_utils


class KakaoView(base.SocialPlatformView, kakao.KakaoContextMixin):
    pass


class KakaoCallBackView(base.SocialPlatformCallBackView, kakao.KakaoContextMixin):
    def _get_user_raw_info(self, access_token) -> Dict:
        return requests.get(
            url=self.profile_url,
            headers={"Authorization": f"Bearer {access_token}"},
        ).json()

    def _get_user_profile(self, user_raw_info: Dict, _: str) -> profile.SocialProfile:
        account_info: Dict = user_raw_info.get("kakao_account")
        email = account_info.get("email")
        username = account_info.get("profile")["nickname"]

        if account_info.get("birthyear_needs_agreement") and account_info.get("birthday_needs_agreement"):
            year = account_info.get("birthyear")
            day = account_info.get("birthday")
            birthdate = time_utils.compact_date_formatter.parse(f"{year}{day}")
        else:
            birthdate = None
        return profile.SocialProfile(email, username, birthdate)


class KakaoLoginView(base.SocialPlatformLoginView, kakao.KakaoContextMixin):
    adapter_class = views.KakaoOAuth2Adapter
