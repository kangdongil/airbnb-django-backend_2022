from django.contrib import admin
from .models import Room, Amenity

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "price",
        "kind",
        "owner",
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