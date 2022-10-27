from django.contrib import admin
from .models import Experience, Perk


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "price",
        "event_start",
        "event_end",
        "host",
    )
    list_filter = (
        "country",
        "city",
        "price",
    )


@admin.register(Perk)
class PerkAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "description",
        "details",
    )