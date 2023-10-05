import math

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PagePagination(PageNumberPagination):
    """Custom pagination class for paginating querysets.

    This class extends the PageNumberPagination class from Django REST framework
    and provides custom settings for pagination.

    - `page_size`: The default page size.
    - `page_size_query_param`: The query parameter for specifying the page size.
    - `max_page_size`: The maximum allowed page size.
    """

    page_size = 5
    page_size_query_param = 'size'
    max_page_size = 20

    def get_paginated_response(self, data):
        """Return a paginated response for a list of data.

        This method constructs a paginated response containing metadata such as the total number of items,
        the total number of pages, links to the previous and next pages, and the data for the current page.

        :param data: The list of data to include in the response.
        :type data: list
        :return: A Response object containing the paginated data and metadata.
        :rtype: Response
        """
        count = self.page.paginator.count
        total_pages = math.ceil(count / self.get_page_size(self.request))
        return Response(
            {
                'total_items': count,
                'total_pages': total_pages,
                'prev': self.get_previous_link(),
                'next': self.get_next_link(),
                'data': data

            }
        )
