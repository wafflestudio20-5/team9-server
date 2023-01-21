import datetime

from rest_framework import exceptions


class DateFormatException(exceptions.APIException):
    status_code = 400
    default_detail = "Unexpected Date(time) format"
    default_code = "ValueError"


class Formatter:
    pattern = NotImplemented

    def parse(self, date_str):
        raise NotImplementedError

    def format(self, date):
        return datetime.datetime.strftime(date, self.pattern)


class DateFormatter(Formatter):
    pattern = NotImplemented

    def parse(self, date_str):
        try:
            return datetime.datetime.strptime(date_str, self.pattern).date()
        except ValueError as e:
            raise DateFormatException from e


class DatetimeFormatter(Formatter):
    pattern = NotImplemented

    def parse(self, date_str):
        return datetime.datetime.strptime(date_str, self.pattern)


class NormalDateFormatter(DateFormatter):
    pattern = "%Y-%m-%d"


class NormalDatetimeFormatter(DatetimeFormatter):
    pattern = "%Y-%m-%d %H:%M:%S"


class CompactDateFormatter(DateFormatter):
    pattern = "%Y%m%d"


normal_date_formatter = NormalDateFormatter()
normal_datetime_formatter = NormalDatetimeFormatter()
compact_date_formatter = CompactDateFormatter()
