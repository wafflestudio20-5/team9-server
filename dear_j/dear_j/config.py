import datetime

# settings regarding login
SITE_ID = 1
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = "username"
ACCOUNT_USERNAME_REQUIRED = True

# custom dj-rest-auth
AUTH_USER_MODEL = "user.User"

# django-allauth
ACCOUNT_ADAPTER = "allauth.account.adapter.DefaultAccountAdapter"

# jwt environment setting
REST_USE_JWT = True
JWT_AUTH_COOKIE = "dearj-auth"
JWT_AUTH_REFRESH_COOKIE = "dearj-refresh-token"
ACCESS_TOKEN_LIFETIME = datetime.timedelta(hours=2)
REFRESH_TOKEN_LIFETIME = datetime.timedelta(days=7)
ROTATE_REFRESH_TOKENS = False
BLACKLIST_AFTER_ROTATION = True

# cors setting
CORS_ORIGIN_ALLOW_ALL = True
