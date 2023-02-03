from rest_framework import exceptions


class SocialLoginEmailException(exceptions.APIException):
    status_code = 400
    default_detail = "Email cannot be duplicated"
    default_code = "ValueError"
