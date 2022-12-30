import json
import os

from django import http
from django import shortcuts
from rest_framework import views

import requests
from user import exceptions
from user import models

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
with open(os.path.join(BASE_DIR, "dear_j/secrets.json"), "rb") as secret_file:
    secrets = json.load(secret_file)


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
                "client_id={client_id}&" +
                "redirect_uri={redirect_uri}&" +
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
                "client_id={client_id}&" +
                "redirect_uri={redirect_uri}&"
                "code={code}"
            )
            token_json = token_request.json()
            error = token_json.get("error", None)
            if error is not None:
                return http.JsonResponse(
                    {"message": "INVALID_CODE"},
                    status=400
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
            kakao_account = profile_json.get("kakao_account")
            email = kakao_account.get("email", None)  # get email
            kakao_id = profile_json.get("id")

        except KeyError:
            return http.JsonResponse(
                {"message": "INVALID_CODE"},
                status=400
            )
        except access_token.DoesNotExist:
            return http.JsonResponse(
                {"message": "INVALID_CODE"},
                status=400
            )
        # login or register to dear j server
        if models.User.objects.filter().exists():
            pass
        else:
            pass
