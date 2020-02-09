from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class MatchHistoryPaginator(PageNumberPagination):
    page_size = 10
    page_size_query_param = "size"
    page_query_param = "page"

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link().replace("", ""),  # old,new
            'previous': self.get_previous_link().replace("", ""),  # old,new
            'count':self.page.paginator.count,
            'result':data
        })
