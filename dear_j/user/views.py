import json
from json import decoder
import os

from django import http
from django import shortcuts
from rest_framework import views as rest_views
from rest_framework import status
from allauth.socialaccount import models as allauth_models
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.google import views as google_view
from allauth.socialaccount.providers.oauth2 import client
from dj_rest_auth.registration import views as auth_views

import requests
from user import exceptions
from user import models

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
with open(os.path.join(BASE_DIR, "dear_j/secrets.json"), "rb") as secret_file:
    secrets = json.load(secret_file)

BASE_URL = "http://127.0.0.1:8000/api/v1/user/"


class KakaoView(rest_views.APIView):
    def get(self, request, format=None):
        try:
            if request.user.is_authenticated:
                raise exceptions.SocialLoginException(
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


class KakaoCallBackView(rest_views.APIView):
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
            """if accept_status != 200:
                return http.JsonResponse(
                    {"message": "failed to signin"},
                    status=accept_status
                )"""
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
            """if accept_status != 200:
                return http.JsonResponse(
                    {"message": "failed to signin"},
                    status=accept_status
                )"""
            accept_json = accept.json()
            accept_json.pop("user", None)
            return http.JsonResponse(accept_json)


class KakaoLogin(auth_views.SocialLoginView):
    adapter_class = kakao_view.KakaoOAuth2Adapter
    client_class = client.OAuth2Client
    callback_url = secrets["KAKAO"]["REDIRECT_URI"]


class GoogleView(rest_views.APIView):
    def get(self, request, format=None):
        info_scope = "https://www.googleapis.com/auth/userinfo.email"
        client_id = secrets["GOOGLE"]["CLIENT_ID"]
        callback_url = secrets["GOOGLE"]["REDIRECT_URI"]
        return shortcuts.redirect(
            f"https://accounts.google.com/o/oauth2/v2/auth?" +
            f"client_id={client_id}&" +
            f"response_type=code&" +
            f"redirect_uri={callback_url}&" +
            f"scope={info_scope}"
        )


class GoogleCallBackView(rest_views.APIView):
    def get(self, request, format=None):
        client_id = secrets["GOOGLE"]["CLIENT_ID"]
        client_pw = secrets["GOOGLE"]["CLIENT_PW"]
        callback_url = secrets["GOOGLE"]["REDIRECT_URI"]
        code = request.GET.get("code")
        state = "state"
        # access token request
        token_request = requests.post(
            f"https://oauth2.googleapis.com/token?" +
            f"client_id={client_id}&" +
            f"client_secret={client_pw}&" +
            f"code={code}&" +
            f"grant_type=authorization_code&" +
            f"redirect_uri={callback_url}&" +
            f"state={state}"
        )
        token_req_json = token_request.json()
        error = token_req_json.get("error")
        if error is not None:
            raise decoder.JSONDecodeError(error)
        access_token = token_req_json.get("access_token")
        # email request
        email_req = requests.get(
            f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")
        email_req_status = email_req.status_code
        if email_req_status != 200:
            return http.JsonResponse({"message": "failed to get email"},
                                     status=status.HTTP_400_BAD_REQUEST)
        email_req_json = email_req.json()
        email = email_req_json.get("email")
        birthdate = email_req_json.get("birthday")
        # signup or signin request
        try:
            print("tried to signin")
            user = models.User.objects.get(email=email)
            print(user)
            social_user = allauth_models.SocialAccount.objects.get(user=user)
            if social_user is None:
                return http.JsonResponse(
                    {"message": "email exists but not social user"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if social_user.provider != "google":
                return http.JsonResponse(
                    {"message": "no matching social type"},
                    status=status.HTTP_400_BAD_REQUEST)
            # google account exist -> sign in
            data = {"access_token": access_token,
                    "code": code}
            accept = requests.post(
                "http://127.0.0.1:8000/api/v1/user/login/google/finish/",
                data=data)
            accept_status = accept.status_code
            if accept_status != 200:
                return http.JsonResponse({"message": "failed to signin"},
                                         status=accept_status)
            accept_json = accept.json()
            accept_json.pop("user", None)
            return http.JsonResponse(accept_json)
        except models.User.DoesNotExist:
            # register user
            data = {"access_token": access_token,
                    "code": code}
            print("user registration finish api call")
            accept = requests.post(
                "http://127.0.0.1:8000/api/v1/user/login/google/finish/",
                data=data
            )
            accept_status = accept.status_code
            if accept_status != 200:
                return http.JsonResponse(
                    {"message": "failed to signup"},
                    status=accept_status
                )
            accept_json = accept.json()
            accept_json.pop("user", None)
            return http.JsonResponse(accept_json)
        except allauth_models.SocialAccount.DoesNotExist:
            return http.JsonResponse(
                {"message": "no matching social type"},
                status=status.HTTP_400_BAD_REQUEST)


class GoogleLogin(auth_views.SocialLoginView):
    adapter_class = google_view.GoogleOAuth2Adapter
    callback_url = "http://127.0.0.1:8000/api/v1/user/login/google/callback/"
    client_class = client.OAuth2Client
