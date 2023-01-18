import datetime
from typing import Dict, List

import requests

from allauth.socialaccount.providers.google import views

from user import models
from user.service.social_login.contexts import google
from user.service.social_login.models import profile
from user.views.social_login import base


class GoogleView(base.SocialPlatformView, google.GoogleContextMixin):
    pass


class GoogleCallBackView(base.SocialPlatformCallBackView, google.GoogleContextMixin):
    def _get_access_token(self, code: str) -> Dict:
        return requests.post(self.get_token_uri(code)).json()

    def _get_user_raw_info(self, access_token: str) -> Dict:
        return requests.get(self.get_email_uri(access_token)).json()

    def _get_user_profile(self, user_raw_info: Dict, access_token: str) -> profile.SocialProfile:
        birthdate_info = requests.get(
            self.get_personal_api_uri("birthdays"),
            headers={"Authorization": f"Bearer {access_token}"},
        ).json()

        email = user_raw_info.get("email")
        birthdate = self._get_birthdate(birthdate_info)
        return profile.SocialProfile(email=email, birthdate=birthdate)

    def _get_birthdate(self, birthdate_raw: Dict):
        raw_data: List[Dict] = birthdate_raw.get("birthdays", [])
        if not raw_data:
            return None
        return datetime.date(**raw_data[0].get("date"))


class GoogleLoginView(base.SocialPlatformLoginView, google.GoogleContextMixin):
    adapter_class = views.GoogleOAuth2Adapter
