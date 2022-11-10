from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = (
        "__str__",
        "event",
        "check_in",
        "check_out",
        "experience_time",
        "guests",
    )
    list_filter = (
        "kind",
    )