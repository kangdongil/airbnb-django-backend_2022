from datetime import datetime
from django.contrib import admin
from . import models
from .filters import PopularityFilter

@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    
    list_display = (
        "__str__",
        "event",
        "booking_date",
        "payload",
        "created_at",
    )
    list_filter = (
        PopularityFilter,
        "rating",
        "user__is_host",
        "room__category",
    )

    def event(self, review):
        return f"{review.category}: {review.event_name}"
    
    def booking_date(self, review):
        if review.room and review.booking:
            return f"{review.booking.check_in} ~ {review.booking.check_out}"
        elif review.experience and review.booking:
            return review.booking.experience_time
        return None
