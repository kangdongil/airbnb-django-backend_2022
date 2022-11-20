from django.contrib import admin
from .models import Photo

@admin.action(description="Set Default Thumbnail Photo")
def assign_default_thumbnail(model_admin, request, photos):
    checked_rooms = []
    checked_experiences = []
    for photo in photos.all():
        if photo.room:
            if photo.room in checked_rooms:
                continue
            checked_rooms.append(photo.room)
            room_photos = Photo.objects.filter(room=photo.room)\
                .order_by("-created_at")
            if room_photos.filter(is_thumbnail=True):
                continue
            thumbnail = room_photos.first()
        elif photo.experience:
            if photo.experience in checked_experiences:
                continue
            checked_experiences.append(photo.experience)
            experience_photos = Photo.objects.filter(experience=photo.experience)\
                .order_by("-created_at")
            if experience_photos.filter(is_thumbnail=True):
                continue
            thumbnail = experience_photos.first()
        thumbnail.is_thumbnail = True
        thumbnail.save()