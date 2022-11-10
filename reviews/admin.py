from datetime import datetime
from django.contrib import admin
from . import models
from .filters import PopularityFilter

@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    
    list_display = (
        "__str__",
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
