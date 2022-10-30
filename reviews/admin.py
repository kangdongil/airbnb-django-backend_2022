from django.contrib import admin
from . import models
from .filters import PopularityFilter

@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    
    list_display = (
        "__str__",
        "category",
        "target_name",
        "payload",
    )
    list_filter = (
        PopularityFilter,
        "rating",
        "user__is_host",
        "room__category",
    )