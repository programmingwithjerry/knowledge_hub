"""
This module defines custom pagination for API responses
using Django REST Framework's PageNumberPagination.
"""

from rest_framework.pagination import PageNumberPagination

class StandardPagination(PageNumberPagination):
    """
    A custom pagination class to standardize the pagination behavior
    for API responses.

    Attributes:
        page_size (int): The default number of items per page.
        page_size_query_param (str): The query parameter that allows
        clients to set a custom page size.
        max_page_size (int): The maximum allowable number of items per
        page to prevent excessive data loads.
    """
    # Default number of items per page
    page_size = 10

    # Query parameter to allow clients to customize the page size
    page_size_query_param = 'page_size'

    # Maximum number of items allowed per page to prevent
    # overloading the server
    max_page_size = 40
