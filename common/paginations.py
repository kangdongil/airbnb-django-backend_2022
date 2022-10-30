from collections import OrderedDict
from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination
from rest_framework.utils.urls import replace_query_param

class ListPagination(PageNumberPagination):

    page_query_param = "page"
    page_size_query_param = "per_page"
    page_size = 5
    max_page_size = 10000


    def get_page_number(self, request):
        try:
            page_number = int(request.query_params.get(
                self.page_query_param, 1
            ))
        except ValueError:
            page_number = 1
        return page_number
    
    def get_page_size(self, request):
        try:
            page_size = int(request.query_params.get(
                self.page_size_query_param, self.page_size
            ))
        except ValueError:
            page_size = self.page_size
        return page_size
    
    def paginate(self, queryset, request):
        page_number = self.get_page_number(request)
        page_size = self.get_page_size(request)

        paginated_queryset = Paginator(queryset, page_size)
        self.page = paginated_queryset.get_page(page_number)
        return list(self.page)
    
    def get_next_link(self):
        if not self.page.has_next():
            return None
        url = self.request.build_absolute_uri()
        page_number = self.page.next_page_number()
        return replace_query_param(
            url,
            self.page_query_param,
            page_number,
        )
    
    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        url = self.request.build_absolute_uri()
        page_number = self.page.previous_page_number()
        return replace_query_param(
            url,
            self.page_query_param,
            page_number
        )
    
    def paginated_info(self):
        return OrderedDict([
            ('active', self.page.number),
            ('pages', self.page.paginator.num_pages),
            ('count', self.page.paginator.count),
            ('previous_link', self.get_previous_link()),
            ('next_link', self.get_next_link()),
        ])