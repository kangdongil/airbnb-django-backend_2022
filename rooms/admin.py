from django.contrib import admin
from .models import Room

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