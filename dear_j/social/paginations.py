from rest_framework import pagination


class NetworkListPagination(pagination.CursorPagination):
    page_size = 20
    ordering = "start_at"
