from rest_framework import pagination


class BlogCustomPagination(pagination.LimitOffsetPagination):
    max_limit = 20
    default_limit = 10
