from urllib import parse


def get_fe_redirect_url(fe_login_url, params):
    url_params = parse.urlencode(params)
    return f"{fe_login_url}?{url_params}"
