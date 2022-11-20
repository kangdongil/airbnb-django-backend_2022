from django.contrib import admin
from .models import Photo, Video
from .actions import assign_default_thumbnail


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    
    actions = (assign_default_thumbnail,)

    list_display = (
        "__str__",
        "event",
        "is_thumbnail",
    )


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    pass