from rest_framework import pagination


class ScheduleListPagination(pagination.CursorPagination):
    page_size = 20
    ordering = "start_at"
