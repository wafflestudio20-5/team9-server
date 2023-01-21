from rest_framework import exceptions


class GetScheduleListKeyException(exceptions.APIException):
    status_code = 400
    default_detail = "email, from, to must be contained in uri params"
    default_code = "KeyError"


class ScheduleDoesNotExistException(exceptions.APIException):
    status_code = 404
    default_detail = "schedule does not exist"
    default_code = "KeyError"
