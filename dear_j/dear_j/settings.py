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

import site_env
from utils import ssm

from dear_j import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
if site_env.is_prod():
    SECRET_KEY = ssm.get_ssm_parameter(alias="/backend/dearj/django-secret-key")
else:
    SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


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
    "dj_rest_auth",
    "dj_rest_auth.registration",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.kakao",
    "allauth.socialaccount.providers.google",
    "user.apps.UserConfig",
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
JWT_AUTH_REFRESH_COOKIE = config.JWT_AUTH_REFRESH_COOKIE
ACCESS_TOKEN_LIFETIME = config.ACCESS_TOKEN_LIFETIME
REFRESH_TOKEN_LIFETIME = config.REFRESH_TOKEN_LIFETIME

# custom dj-rest-auth (for birthday/username field)
REST_AUTH_SERIALIZERS = {"USER_DETAILS_SERIALIZER": "user.serializers.CustomUserDetailSerializer"}
REST_AUTH_REGISTER_SERIALIZERS = {"REGISTER_SERIALIZER": "user.serializers.CustomRegisterSerializer"}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": ACCESS_TOKEN_LIFETIME,
    "REFRESH_TOKEN_LIFETIME": REFRESH_TOKEN_LIFETIME,
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
}


MIDDLEWARE = [
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

if site_env.is_prod():
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": "database-dear-j",
            "USER": "admin",
            "PASSWORD": ssm.get_ssm_parameter("/database/dearj/master_key"),
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

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
