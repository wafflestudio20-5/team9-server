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
