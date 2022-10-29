from rest_framework.serializers import ModelSerializer
from .models import Room


class RoomListSerializer(ModelSerializer):
    class Meta:
        model=Room
        fields=(
            "pk",
            "name",
            "country",
            "city",
            "price",
        )


class RoomDetailSerializer(ModelSerializer):
    class Meta:
        model=Room
        fields= "__all__"