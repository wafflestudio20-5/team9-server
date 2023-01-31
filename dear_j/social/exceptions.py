from rest_framework import exceptions


class FollowAcceptOrRejectAPIException(exceptions.APIException):
    status_code = 400
    default_detail = "Only Approved State can be changed"
    default_code = "KeyError"
