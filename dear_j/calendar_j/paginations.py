import collections

from rest_framework import pagination
from rest_framework import response as resp


class ScheduleListPagination(pagination.CursorPagination):
    page_size = 20
    ordering = "start_at"

    def get_paginated_response(self, data, **kwargs):
        return resp.Response(
            collections.OrderedDict([("next", self.get_next_link()), ("previous", self.get_previous_link()), ("results", data)]), **kwargs
        )
