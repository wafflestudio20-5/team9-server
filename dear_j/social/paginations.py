from rest_framework import pagination


class CandidateListPagination(pagination.CursorPagination):
    page_size = 20
    ordering = "email"


class NetworkListPagination(pagination.CursorPagination):
    page_size = 20
    ordering = "created_at"
