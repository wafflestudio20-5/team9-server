import json
from json import decoder
import os
from urllib import parse

from django import http
from django import shortcuts
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework import views as rest_views

from allauth.socialaccount import adapter
from allauth.socialaccount import models as allauth_models
from allauth.socialaccount.providers.google import views as google_view
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.oauth2 import client
from dj_rest_auth.registration import views as auth_views
import requests
from user import exceptions
from user import models
from user import serializers

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
with open(os.path.join(BASE_DIR, "dear_j/secrets.json"), "rb") as secret_file:
    secrets = json.load(secret_file)

BASE_URL = "http://127.0.0.1:8000/api/v1/user/"
BASE_FRONTEND_URL = "http://127.0.0.1:3000"

class KakaoView(rest_views.APIView):
    def get(self, request, format=None):
        fe_login_url = f"{BASE_FRONTEND_URL}/login"
        try:
            if request.user.is_authenticated:
                params = parse.urlencode({
                    "error":"user_already_logged_in"
                })
                return shortcuts.redirect(f"{fe_login_url}?{params}")
            client_id = secrets["KAKAO"]["REST_API_KEY"]
            redirect_uri = secrets["KAKAO"]["REDIRECT_URI"]
            return shortcuts.redirect(
                f"https://kauth.kakao.com/oauth/authorize?" +
                f"client_id={client_id}&" +
                f"redirect_uri={redirect_uri}&" +
                "response_type=code"
            )
        except exceptions.KakaoException as error:
            params = parse.urlencode({
                "error":"kakao_exception"
            })
            return shortcuts.redirect(f"{fe_login_url}?{params}")
        except exceptions.SocialLoginException as error:
            params = parse.urlencode({
                "error":"social_login_exception"
            })
            return shortcuts.redirect(f"{fe_login_url}?{params}")


class KakaoCallBackView(rest_views.APIView):
    def get(self, request, format=None):
        fe_login_url = f"{BASE_FRONTEND_URL}/login"
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
            error = token_json.get("error")
            if error is not None:
                params = parse.urlencode({
                    "error":"invalid-KAKAO-token"
                })
                return shortcuts.redirect(f"{fe_login_url}?{params}")

            access_token = token_json.get("access_token")
            # use access token to get kakao profile info
            profile_request = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={
                    "Authorization": f"Bearer {access_token}"
                }
            )
            profile_json = profile_request.json()
            error = profile_json.get("error")
            if error is not None:
                params = parse.urlencode({
                    "error":"invalid-profile-request-token"
                })
                return shortcuts.redirect(f"{fe_login_url}?{params}")

            kakao_account = profile_json.get("kakao_account")
            # required
            email = kakao_account.get("email")
            # not required field
            birthday = "9999-12-31"
            if "birthday" in kakao_account.keys():
                raw_mmdd = kakao_account.get("birthday")
                birthday = "9999-" + raw_mmdd[:2] + "-" + raw_mmdd[2:]
            username = "user"
            if "nickname" in kakao_account.keys():
                username = kakao_account.get("profile").get("nickname")
            
        except KeyError:
            params = parse.urlencode({
                    "error":"invalid-code"
                })
            return shortcuts.redirect(f"{fe_login_url}?{params}")

        except access_token.DoesNotExist:
            params = parse.urlencode({
                    "error":"invalid-code"
                })
            return shortcuts.redirect(f"{fe_login_url}?{params}")

        # signup or signin
        try:
            user = models.User.objects.get(email=email)
            # check if the provider of the user is kakao
            social_user = allauth_models.SocialAccount.objects.get(user=user)
            if social_user is None:
                params = parse.urlencode({
                    "error":"Email-exists-but-not-social-user"
                })
                return shortcuts.redirect(f"{fe_login_url}?{params}")

            if social_user.provider != "kakao":
                params = parse.urlencode({
                    "error":"Email-exists-but-not-kakao-user"
                })
                return shortcuts.redirect(f"{fe_login_url}?{params}")

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
                params = parse.urlencode({
                    "error":"failed-to-signin"
                })
                return shortcuts.redirect(f"{fe_login_url}?{params}")

            accept_json = accept.json()
            accept_json.pop('user', None)
            params = parse.urlencode(accept_json)
            return shortcuts.redirect(f"{fe_login_url}?{params}")

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
                params = parse.urlencode({
                    "error":"failed-to-register"
                })
                return shortcuts.redirect(f"{fe_login_url}?{params}")

            accept_json = accept.json()
            accept_json.pop('user', None)
            new_user = models.User.objects.get(email=email)
            if birthday != "9999-12-31":
                new_user.birthday = birthday
                new_user.save()
            params = parse.urlencode(accept_json)
            return shortcuts.redirect(f"{fe_login_url}?{params}")
        
        except allauth_models.SocialAccount.DoesNotExist:
            params = parse.urlencode({
                    "error":"Email-exists-but-not-kakao-user"
                })
            return shortcuts.redirect(f"{fe_login_url}?{params}")



class KakaoLogin(auth_views.SocialLoginView):
    adapter_class = kakao_view.KakaoOAuth2Adapter
    client_class = client.OAuth2Client
    callback_url = secrets["KAKAO"]["REDIRECT_URI"]


class GoogleView(rest_views.APIView):
    def get(self, request, format=None):
        info_scope = "https://www.googleapis.com/auth/user.birthday.read https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile"
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
        fe_login_url = f"{BASE_FRONTEND_URL}/login"
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
            params = parse.urlencode({
                    "error":"failed-to-get-email"
                })
            return shortcuts.redirect(f"{fe_login_url}?{params}")
        
        email_req_json = email_req.json()
        email = email_req_json.get("email")
        birthday_req = requests.get(
                "https://people.googleapis.com/v1/people/me?personFields=birthdays",
                headers={
                    "Authorization": f"Bearer {access_token}"
                }
            )
        birthday = "9999-12-31"
        birthday_json = birthday_req.json()
        if birthday_json.get("birthdays") is not None:
            if birthday_json.get("birthdays")[0].get("date") is not None:
                date = birthday_json.get("birthdays")[0].get("date")
                year = str(date.get("year")).rjust(4, "0")
                month = str(date.get("month")).rjust(2, "0")
                day = str(date.get("day")).rjust(2, "0")
                birthday = year + "-" + month + "-" + day
        # signup or signin request
        try:
            user = models.User.objects.get(email=email)
            social_user = allauth_models.SocialAccount.objects.get(user=user)
            if social_user is None:
                params = parse.urlencode({
                    "error":"email-exists-but-not-social-user"
                })
                return shortcuts.redirect(f"{fe_login_url}?{params}")
            
            if social_user.provider != "google":
                params = parse.urlencode({
                    "error":"no-matching-social-type"
                })
                return shortcuts.redirect(f"{fe_login_url}?{params}")
            # google account exist -> sign in
            data = {"access_token": access_token,
                    "code": code}
            accept = requests.post(
                "http://127.0.0.1:8000/api/v1/user/login/google/finish/",
                data=data)
            accept_status = accept.status_code
            if accept_status != 200:
                params = parse.urlencode({
                    "error":"failed-to-signin"
                })
                return shortcuts.redirect(f"{fe_login_url}?{params}")
            accept_json = accept.json()
            accept_json.pop('user', None)
            params = parse.urlencode(accept_json)
            return shortcuts.redirect(f"{fe_login_url}?{params}")
        except models.User.DoesNotExist:
            # register user
            data = {"access_token": access_token,
                    "code": code}
            accept = requests.post(
                "http://127.0.0.1:8000/api/v1/user/login/google/finish/",
                data=data
            )
            accept_status = accept.status_code
            if accept_status != 200:
                params = parse.urlencode({
                    "error":"failed-to-signup"
                })
                return shortcuts.redirect(f"{fe_login_url}?{params}")
            user = models.User.objects.get(email=email)
            if birthday != "9999-12-31":
                user.birthday = birthday
                user.save()
            accept_json = accept.json()
            accept_json.pop('user', None)
            params = parse.urlencode(accept_json)
            return shortcuts.redirect(f"{fe_login_url}?{params}")

        except allauth_models.SocialAccount.DoesNotExist:
            params = parse.urlencode({
                    "error":"no-matching-social-type"
                })
            return shortcuts.redirect(f"{fe_login_url}?{params}")

class GoogleLogin(auth_views.SocialLoginView):
    # process login
    adapter_class = google_view.GoogleOAuth2Adapter
    callback_url = "http://127.0.0.1:8000/api/v1/user/login/google/callback/"
    client_class = client.OAuth2Client

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.CustomUserDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_object(self):
        return self.request.user
