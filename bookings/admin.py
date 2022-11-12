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
        "is_valid",
        "is_confirmed",
        "booking_state",
    )

    list_filter = ("kind",)

    def event(self, booking):
        return f"{booking.kind.title()}: {booking.event_name}"

    def is_valid(self, booking):
        return not booking.is_cancelled
    is_valid.boolean = True

    def is_confirmed(self, booking):
        host_approval_state = booking.host_approval_state
        match = {
            "pending": None,
            "confirmed": True,
            "denied": False,
        }
        return match.get(host_approval_state)
    is_confirmed.boolean = True