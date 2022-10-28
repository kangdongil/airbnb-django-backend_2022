from django.contrib import admin
from .models import Room, Amenity
from .actions import adjust_prices

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    actions = (adjust_prices,)

    list_display = (
        "name",
        "price",
        "kind",
        "owner",
        "total_amenities",
        "average_ratings",
    )

    list_filter = (
        "country",
        "city",
        "price",
        "rooms",
        "toilets",
        "kind",
    )

    search_fields = (
        "owner__username",
        "=price",
    )
    search_help_text = "Search by Owner Username First, then exact price later"

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "description",
        "created",
        "updated",
    )
    readonly_fields = (
        "created",
        "updated",
    )