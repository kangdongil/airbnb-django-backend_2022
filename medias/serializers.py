from rest_framework.serializers import ModelSerializer
from .models import Photo, Video


class PhotoSerializer(ModelSerializer):
    class Meta:
        model = Photo
        fields = (
            "pk",
            "file",
            "description",
        )


class VideoSerializer(ModelSerializer):
    class Meta:
        model = Video
        fields = (
            "pk",
            "file",
            "description",
        )