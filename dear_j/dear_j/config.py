import datetime
import os

import site_env
from utils import ssm as ssm_utils

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
ACCOUNT_ADAPTER = "user.adapter.AccountAdapter"
if site_env.is_test():
    KAKAO_CLIENT_ID = os.environ.get("KAKAO_CLIENT_ID")
    KAKAO_SECRET = os.environ.get("KAKAO_SECRET")
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_SECRET = os.environ.get("GOOGLE_SECRET")
else:
    KAKAO_CLIENT_ID = ssm_utils.get_ssm_parameter(alias="/backend/dearj/kakao/client-id")
    KAKAO_SECRET = ssm_utils.get_ssm_parameter(alias="/backend/dearj/kakao/client-pw")
    GOOGLE_CLIENT_ID = ssm_utils.get_ssm_parameter(alias="/backend/dearj/google/client-id")
    GOOGLE_SECRET = ssm_utils.get_ssm_parameter(alias="/backend/dearj/google/client-pw")

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

# aws setting
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
AWS_S3_SECURE_URLS = False
AWS_QUERYSTRING_AUTH = False

AWS_REGION = "ap-northeast-2"
if site_env.is_test():
    AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
else:
    AWS_STORAGE_BUCKET_NAME = ssm_utils.get_ssm_parameter(alias="/backend/dearj/s3/blog")
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com"
AWS_S3_OBJECT_PARAMETERS = {}
