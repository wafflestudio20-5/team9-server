from rest_framework import exceptions


class GetScheduleListKeyException(exceptions.APIException):
    status_code = 400
    default_detail = "email, from, to must be contained in uri params"
    default_code = "KeyError"
