import json
import os

from django import http
from django import shortcuts
from rest_framework import views
from rest_framework import status
from allauth.socialaccount import models as allauth_models
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.oauth2 import client
from dj_rest_auth.registration import views

import requests
from user import exceptions
from user import models

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
with open(os.path.join(BASE_DIR, "dear_j/secrets.json"), "rb") as secret_file:
    secrets = json.load(secret_file)

BASE_URL = "http://127.0.0.1:8000/"


class KakaoView(views.APIView):
    def get(self, request, format=None):
        try:
            if request.user.is_authenticated:
                raise exceptions.SocialLoginExeption(
                    "User already logged in."
                )
            client_id = secrets["KAKAO"]["REST_API_KEY"]
            redirect_uri = secrets["KAKAO"]["REDIRECT_URI"]
            return shortcuts.redirect(
                f"https://kauth.kakao.com/oauth/authorize?" +
                f"client_id={client_id}&" +
                f"redirect_uri={redirect_uri}&" +
                "response_type=code"
            )
        except exceptions.KakaoException as error:
            return shortcuts.redirect("http://127.0.0.1:8000")
        except exceptions.SocialLoginException as error:
            return shortcuts.redirect("http://127.0.0.1:8000")


class KakaoCallBackView(views.APIView):
    def get(self, request, format=None):
        try:
            # get authorization code from kakao server
            code = request.GET.get("code")
            client_id = secrets["KAKAO"]["REST_API_KEY"]
            redirect_uri = secrets["KAKAO"]["REDIRECT_URI"]
            # get access token from kakao server
            token_request = requests.get(
                f"https://kauth.kakao.com/oauth/token?" +
                "grant_type=authorization_code&" +
                f"client_id={client_id}&" +
                f"redirect_uri={redirect_uri}&"
                f"code={code}"
            )
            token_json = token_request.json()
            error = token_json.get("error", None)
            if error is not None:
                return http.JsonResponse(
                    {"message": "INVALID_CODE"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            access_token = token_json.get("access_token")
            # use access token to get kakao profile info
            profile_request = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={
                    "Authorization": f"Bearer {access_token}"
                },
            )
            profile_json = profile_request.json()
            error = profile_json.get("error")
            if error is not None:
                return http.JsonResponse(
                    {"message": "INVALID_CODE"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            kakao_account = profile_json.get("kakao_account")
            email = kakao_account.get("email", None)  # get email
            kakao_id = profile_json.get("id")

        except KeyError:
            return http.JsonResponse(
                {"message": "INVALID_CODE"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except access_token.DoesNotExist:
            return http.JsonResponse(
                {"message": "INVALID_CODE"},
                status=status.HTTP_400_BAD_REQUEST
            )
        # signup or signin
        try:
            user = models.User.objects.get(email=email)
            # check if the provider of the user is kakao
            social_user = allauth_models.SocialAccount.objects.get(user=user)
            if social_user is None:
                return http.JsonResponse(
                    {
                        "message": "Email exists but not social user"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            if social_user.provider != "kakao":
                return http.JsonResponse(
                    {
                        "message": "Email exists but not kakao user"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            # kakao users that registered earlier
            data = {
                "access_token": access_token,
                "code": code
            }
            accept = requests.post(
                f"{BASE_URL}login/kakao/finish/",
                data=data
            )
            accept_status = accept.status_code
            if accept_status != 200:
                return http.JsonResponse(
                    {"message": "failed to signin"},
                    status=accept_status
                )
            accept_json = accept.json()
            accept_json.pop("user", None)
            return http.JsonResponse(accept_json)

        except models.User.DoesNotExist:
            # kakao user does not exist
            data = {
                "access_token": access_token,
                "code": code
            }
            accept = requests.post(
                f"{BASE_URL}login/kakao/finish/",
                data=data
            )
            accept_status = accept.status_code
            if accept_status != 200:
                return http.JsonResponse(
                    {"message": "failed to signin"},
                    status=accept_status
                )
            accept_json = accept.json()
            accept_json.pop("user", None)
            return http.JsonResponse(accept_json)


class KakaoLogin(views.SocialLoginView):
    adapter_class = kakao_view.KakaoOAuth2Adapter
    client_class = client.OAuth2Client
    callback_url = secrets["KAKAO"]["REDIRECT_URI"]
