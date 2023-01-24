from rest_framework import pagination


class PostListPagination(pagination.CursorPagination):
    page_size = 10
    ordering = "-created_at"


class CommentListPagination(pagination.CursorPagination):
    page_size = 10
    ordering = "-created_at"
