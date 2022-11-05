from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Room, Amenity
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer


class AmenitySerializer(ModelSerializer):
    class Meta:
        model=Amenity
        fields="__all__"


class RoomListSerializer(ModelSerializer):

    rating = SerializerMethodField()
    is_owner = SerializerMethodField()

    class Meta:
        model=Room
        fields=(
            "pk",
            "name",
            "country",
            "city",
            "price",
            "rating",
            "is_owner",
        )
    
    def get_rating(self, room):
        return room.average_ratings()

    def get_is_owner(self, room):
        request = self.context["request"]
        return room.owner == request.user

class RoomDetailSerializer(ModelSerializer):
    
    owner=TinyUserSerializer(read_only=True)
    category=CategorySerializer(read_only=True)
    total_reviews = SerializerMethodField()
    total_amenities = SerializerMethodField()
    total_photos = SerializerMethodField()

    class Meta:
        model=Room
        exclude=("amenities",)
    
    def get_total_amenities(self, room):
        return room.total_amenities()

    def get_total_reviews(self, room):
        return room.total_reviews()

    def get_total_photos(self, room):
        return room.total_photos()