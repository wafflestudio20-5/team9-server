"""
Django settings for dear_j project.
Generated by 'django-admin startproject' using Django 4.1.1.
For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
import pathlib

import pymysql

from dear_j import config
from dear_j import host
import site_env
from utils import ssm as ssm_utils
from utils import time as time_utils

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

if site_env.is_test():
    SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
else:
    SECRET_KEY = ssm_utils.get_ssm_parameter(alias="/backend/dearj/django-secret-key")
DEBUG = True  # not site_env.is_prod()

ALLOWED_HOSTS = host.BACKEND_HOST.ALLOWED_HOSTS

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https") if site_env.is_prod_or_stage() else None

BACKEND_URL = host.BACKEND_HOST.url
FRONTEND_URL = host.FRONTEND_HOST.url
DOMAIN = host.BACKEND_HOST.domain
NAME = host.BACKEND_HOST.get_name()


# drf spectacular setting
SPECTACULAR_SETTINGS = {
    "TITLE": "J-Calendar API Document",
    "DESCRIPTION": "API document of Calendar J by drf-spectacular",
    "SWAGGER_UI_SETTINGS": {
        "persistAuthorization": True,
        "displayOperationId": True,
        "filter": True,
    },
}

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "dj_rest_auth",
    "dj_rest_auth.registration",
    "django_s3_storage",
    "drf_spectacular",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.kakao",
    "calendar_j.apps.CalendarJConfig",
    "blog.apps.BlogConfig",
    "user.apps.UserConfig",
    "social.apps.SocialConfig",
    "documentation.apps.DocumentationConfig",
]


# rest framework setting
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.CursorPagination",
    "PAGE_SIZE": 100,
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.AllowAny",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "dj_rest_auth.jwt_auth.JWTCookieAuthentication",
    ),
    "DATE_FORMAT": time_utils.NormalDateFormatter.pattern,
    "DATETIME_FORMAT": time_utils.NormalDatetimeFormatter.pattern,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# settings regarding login
SITE_ID = config.SITE_ID
ACCOUNT_UNIQUE_EMAIL = config.ACCOUNT_UNIQUE_EMAIL
ACCOUNT_USER_MODEL_USERNAME_FIELD = config.ACCOUNT_USER_MODEL_USERNAME_FIELD
ACCOUNT_USERNAME_REQUIRED = config.ACCOUNT_USERNAME_REQUIRED
ACCOUNT_EMAIL_REQUIRED = config.ACCOUNT_EMAIL_REQUIRED
ACCOUNT_AUTHENTICATION_METHOD = config.ACCOUNT_AUTHENTICATION_METHOD
ACCOUNT_EMAIL_VERIFICATION = config.ACCOUNT_EMAIL_VERIFICATION

# custom dj-rest-auth
AUTH_USER_MODEL = config.AUTH_USER_MODEL
ACCOUNT_ADAPTER = config.ACCOUNT_ADAPTER

# jwt environment setting
REST_USE_JWT = config.REST_USE_JWT
# JWT_AUTH_COOKIE = config.JWT_AUTH_COOKIE # if use this, refresh token is needed to logout
JWT_AUTH_REFRESH_COOKIE = config.JWT_AUTH_REFRESH_COOKIE
ACCESS_TOKEN_LIFETIME = config.ACCESS_TOKEN_LIFETIME
REFRESH_TOKEN_LIFETIME = config.REFRESH_TOKEN_LIFETIME
ROTATE_REFRESH_TOKENS = config.ROTATE_REFRESH_TOKENS
BLACKLIST_AFTER_ROTATION = config.BLACKLIST_AFTER_ROTATION

# cors setting
CORS_ORIGIN_ALLOW_ALL = config.CORS_ORIGIN_ALLOW_ALL

# Test COOP
SECURE_CROSS_ORIGIN_OPENER_POLICY = None

# custom dj-rest-auth serializer
REST_AUTH_SERIALIZERS = {"USER_DETAILS_SERIALIZER": "user.serializers.UserDetailSerializer"}
REST_AUTH_REGISTER_SERIALIZERS = {"REGISTER_SERIALIZER": "user.serializers.RegisterSerializer"}

# aws settings
DEFAULT_FILE_STORAGE = config.DEFAULT_FILE_STORAGE
AWS_S3_SECURE_URLS = config.AWS_S3_SECURE_URLS
AWS_QUERYSTRING_AUTH = config.AWS_QUERYSTRING_AUTH

AWS_REGION = config.AWS_REGION
AWS_STORAGE_BUCKET_NAME = config.AWS_STORAGE_BUCKET_NAME
AWS_S3_CUSTOM_DOMAIN = config.AWS_S3_CUSTOM_DOMAIN
AWS_S3_OBJECT_PARAMETERS = config.AWS_S3_OBJECT_PARAMETERS
MEDIA_ROOT = os.path.join(BASE_DIR, "path/to/store/my/files/")


# allauth setting : https://django-allauth.readthedocs.io/en/latest/configuration.html
# Check get_app function in allauth.socialaccount.adapter.py
SOCIALACCOUNT_PROVIDERS = {
    "kakao": {
        "APP": {
            "client_id": config.KAKAO_CLIENT_ID,
            "secret": config.KAKAO_SECRET,
            "key": "",
        },
    },
    "google": {
        "APP": {
            "client_id": config.GOOGLE_CLIENT_ID,
            "secret": config.GOOGLE_SECRET,
            "key": "",
        },
    },
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": ACCESS_TOKEN_LIFETIME,
    "REFRESH_TOKEN_LIFETIME": REFRESH_TOKEN_LIFETIME,
    "ROTATE_REFRESH_TOKENS": ROTATE_REFRESH_TOKENS,
    "BLACKLIST_AFTER_ROTATION": BLACKLIST_AFTER_ROTATION,
}


AUTHENTICATION_BACKENDS = ("django.contrib.auth.backends.ModelBackend", "allauth.account.auth_backends.AuthenticationBackend")

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "dear_j.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "dear_j.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

if site_env.is_prod_or_stage():
    pymysql.install_as_MySQLdb()
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": "dear_j" if site_env.is_prod() else "dear_j_stage",
            "USER": "admin",
            "PASSWORD": ssm_utils.get_ssm_parameter("/database/dearj/master_key"),
            "HOST": "database-dear-j.c8csrf4cdshb.ap-northeast-2.rds.amazonaws.com",
            "PORT": "3306",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR.parent, "static/")


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
