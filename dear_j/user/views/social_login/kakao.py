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
    def _get_access_token(self, code: str) -> Dict:
        headers = {"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"}
        return requests.post(self.get_token_uri(code), headers=headers).json()

    def _get_user_raw_info(self, access_token) -> Dict:
        headers = {
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
            "Authorization": f"Bearer {access_token}",
        }
        return requests.get(
            url=self.profile_url,
            headers=headers,
        ).json()

    def _get_user_profile(self, user_raw_info: Dict, _: str) -> profile.SocialProfile:
        account_info: Dict = user_raw_info.get("kakao_account")
        email = account_info.get("email")
        username = account_info.get("profile")["nickname"]

        has_birthyear = "birthyear" in account_info.keys()
        has_birthday = "birthday" in account_info.keys()

        birthyear = int(account_info.get("birthyear")) if has_birthyear else None
        birthday = int(account_info.get("birthday")) if has_birthday else None

        birthdate = None
        if has_birthyear and has_birthday:
            birthdate = time_utils.compact_date_formatter.parse(f"{birthyear}{birthday}")
        return profile.SocialProfile(email, username, birthdate, birthyear, birthday)


class KakaoLoginView(base.SocialPlatformLoginView, kakao.KakaoContextMixin):
    adapter_class = views.KakaoOAuth2Adapter
