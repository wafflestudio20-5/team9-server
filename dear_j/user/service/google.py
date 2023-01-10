from allauth.socialaccount import models as allauth_models
from user import models

def google_oauth_string(GOOGLE_CLIENT_ID, GOOGLE_REDIRECT_URI):
    info_scope = "https://www.googleapis.com/auth/user.birthday.read https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile"
    return f"https://accounts.google.com/o/oauth2/v2/auth?" + \
            f"client_id={GOOGLE_CLIENT_ID}&" + \
            f"response_type=code&" + \
            f"redirect_uri={GOOGLE_REDIRECT_URI}&" + \
            f"scope={info_scope}"

def google_token_string(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_PW, GOOGLE_REDIRECT_URI, code):
    return f"https://oauth2.googleapis.com/token?" + \
            f"client_id={GOOGLE_CLIENT_ID}&" + \
            f"client_secret={GOOGLE_CLIENT_PW}&" + \
            f"code={code}&" + \
            f"grant_type=authorization_code&" + \
            f"redirect_uri={GOOGLE_REDIRECT_URI}&" + \
            f"state=state"

def google_email_request(access_token):
    return f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}"

def get_email(email_req):
    return email_req.json().get("email")

def get_birthday(birthday_req):
    birthday = "9999-12-31"
    birthday_json = birthday_req.json()
    if birthday_json.get("birthdays") is not None:
        if birthday_json.get("birthdays")[0].get("date") is not None:
            date = birthday_json.get("birthdays")[0].get("date")
            year = str(date.get("year")).rjust(4, "0")
            month = str(date.get("month")).rjust(2, "0")
            day = str(date.get("day")).rjust(2, "0")
            birthday = year + "-" + month + "-" + day
    return birthday

def check_user_type(email):
    user = models.User.objects.get(email=email)
    social_user = allauth_models.SocialAccount.objects.get(user=user)
    if social_user is None:
        return "general_user"
    elif social_user.provider != "google":
        return "kakao_user"
    else:
        return "google_user"