from urllib import parse


def get_fe_redirect_url(fe_login_url, params):
    url_params = parse.urlencode(params)
    return f"{fe_login_url}?{url_params}"

def token_error_occur(token_json):
    if token_json.get("error") is not None:
        return True
    else:
        return False
    
def response_error_occur(response):
    if response.status_code != 200:
        return True
    else:
        return False