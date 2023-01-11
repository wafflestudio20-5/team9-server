from urllib import parse


def get_fe_redirect_url(fe_login_url, params):
    url_params = parse.urlencode(params)
    return f"{fe_login_url}?{url_params}"


def token_error_occur(token_json):
    return token_json.get("error") is not None


def response_error_occur(response):
    return response.status_code != 200
