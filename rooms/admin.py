from django.contrib import admin
from .models import Room, Amenity
from .actions import adjust_prices_100

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    actions = (adjust_prices,)

    list_display = (
        "name",
        "price",
        "kind",
        "owner",
        "total_amenities",
    )

    list_filter = (
        "country",
        "city",
        "price",
        "rooms",
        "toilets",
        "kind",
    )


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