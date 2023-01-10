def kauth_authorize_string(client_id, redirect_uri):
    return f"https://kauth.kakao.com/oauth/authorize?" + \
            f"client_id={client_id}&" + \
            f"redirect_uri={redirect_uri}&" + \
            "response_type=code"

def kauth_token_string(client_id, redirect_uri, code):
    return f"https://kauth.kakao.com/oauth/token?" + \
            "grant_type=authorization_code&" + \
            f"client_id={client_id}&" + \
            f"redirect_uri={redirect_uri}&" \
            f"code={code}"


def get_email(profile_json):
    return profile_json.get("kakao_account").get("email")

def get_birthday(profile_json):
    birthday = "9999-12-31"
    kakao_account = profile_json.get("kakao_account")
    if "birthday" in kakao_account.keys():
            raw_mmdd = kakao_account.get("birthday")
            birthday = "9999-" + raw_mmdd[:2] + "-" + raw_mmdd[2:]
    return birthday
    
def get_username(profile_json):
    username = "user"
    kakao_account = profile_json.get("kakao_account")
    if "nickname" in kakao_account.keys():
        username = kakao_account.get("profile").get("nickname")
    return username