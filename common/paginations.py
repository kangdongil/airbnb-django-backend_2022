from collections import OrderedDict
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework.utils.urls import replace_query_param


class ListPagination:

    page_query_param = "page"
    page_size_query_param = "per_page"
    page_size = 5


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
    
    @property
    def paginated_info(self):
        return OrderedDict([
            ('active', self.page.number),
            ('pages', self.page.paginator.num_pages),
            ('count', self.page.paginator.count),
            ('previous_link', self.get_previous_link()),
            ('next_link', self.get_next_link()),
        ])


class MonthlyBookingPagination:

    booking_date_query_param = "booking_date"

    def get_booking_date(self, request):
        now = timezone.localtime(timezone.now()).date()
        param_value = request.query_params.get(
            self.booking_date_query_param,
            None,
        )
        try:
            booking_date = datetime.strptime(
                param_value, "%Y-%m"
            )
        except (TypeError, ValueError):
            booking_date = now.replace(day=1)
        self.booking_date = booking_date
        return booking_date

    def paginate(self, queryset, request):
        booking_date = self.get_booking_date(request)
        paginated_queryset = queryset.filter(
            (
                (
                    Q(check_in__lt=booking_date) |
                    Q(check_in__month=booking_date.month)
                ) &
                Q(check_out__gte=booking_date)
            ) | (
                Q(experience_time__month = booking_date.month)
            )
        )
        self.total_data = paginated_queryset.count()
        return list(paginated_queryset)

    def get_previous_link(self):
        url = self.request.build_absolute_uri()
        previous_month = datetime.strftime(
            self.booking_date + relativedelta(months=-1),
            "%Y-%m",
        )
        return replace_query_param(
            url,
            self.booking_date_query_param,
            previous_month,
        )

    def get_next_link(self):
        url = self.request.build_absolute_uri()
        next_month = datetime.strftime(
            self.booking_date + relativedelta(months=1),
            "%Y-%m",
        )
        return replace_query_param(
            url,
            self.booking_date_query_param,
            next_month,
        )

    @property
    def paginated_info(self):
        active_page = datetime.strftime(
            self.booking_date, "%Y-%m"
        )
        return OrderedDict([
            ('active', active_page),
            ('count', self.total_data),
            ('previous_link', self.get_previous_link()),
            ('next_link', self.get_next_link()),
        ])