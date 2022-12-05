from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Room, Amenity
from common.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer
from medias.models import Photo
from medias.serializers import PhotoSerializer
from reviews.serializers import ReviewSerializer
from wishlists.models import Wishlist


class AmenitySerializer(ModelSerializer):
    class Meta:
        model=Amenity
        fields="__all__"


class HostRoomSerializer(ModelSerializer):

    preview_photo = SerializerMethodField()
    rating = SerializerMethodField()
    total_reviews = SerializerMethodField()

    class Meta:
        model=Room
        fields=(
            "pk",
            "name",
            "preview_photo",
            "kind",
            "rating",
            "total_reviews",
        )
    
    def get_rating(self, room):
        return room.average_ratings()
    
    def get_total_reviews(self, room):
        return room.total_reviews()
    
    def get_preview_photo(self, room):
        try:
            preview_photo = Photo.objects.get(
                room=room,
                is_thumbnail=True,
            )
        except Photo.DoesNotExist:
            return
        return PhotoSerializer(preview_photo).data


class WishlistRoomSerializer(ModelSerializer):

    photos = PhotoSerializer(
        read_only=True,
        many=True,
    )
    is_liked = SerializerMethodField()

    class Meta:
        model=Room
        fields=(
            "pk",
            "name",
            "price",
            "rooms",
            "toilets",
            "photos",
            "is_liked",
        )

    def get_is_liked(self, room):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Wishlist.objects.filter(
            owner=request.user,
            rooms__pk=room.pk,
            ).exists()
        return False


class RoomListSerializer(ModelSerializer):

    rating = SerializerMethodField()
    preview_photo = SerializerMethodField()
    is_owner = SerializerMethodField()
    is_liked = SerializerMethodField()

    class Meta:
        model=Room
        fields=(
            "pk",
            "name",
            "country",
            "city",
            "price",
            "rating",
            "preview_photo",
            "is_owner",
            "is_liked",
        )
    
    def get_rating(self, room):
        return room.average_ratings()

    def get_is_owner(self, room):
        request = self.context["request"]
        return room.owner == request.user

    def get_is_liked(self, room):
        request = self.context["request"]
        if request.user.is_authenticated:
            return Wishlist.objects.filter(
            owner=request.user,
            rooms__pk=room.pk,
            ).exists()
        return False
    
    def get_preview_photo(self, room):
        try:
            preview_photo = Photo.objects.get(
                room=room,
                is_thumbnail=True,
            )
        except Photo.DoesNotExist:
            return
        return PhotoSerializer(preview_photo).data


class RoomDetailSerializer(ModelSerializer):
    
    owner = TinyUserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    reviews = ReviewSerializer(
        read_only=True,
        many=True,
    )
    amenities = AmenitySerializer(
        read_only=True,
        many=True,
    )
    photos = PhotoSerializer(
        read_only=True,
        many=True,
    )
    rating = SerializerMethodField()
    total_reviews = SerializerMethodField()
    is_liked = SerializerMethodField()

    class Meta:
        model=Room
        fields = "__all__"

    def get_total_reviews(self, room):
        return room.total_reviews()

    def get_rating(self, room):
        rating = room.average_ratings()
        return f"{rating:.2f}"

    def get_is_liked(self, room):
        request = self.context["request"]
        if request.user.is_authenticated:
            return Wishlist.objects.filter(
            owner=request.user,
            rooms__pk=room.pk,
            ).exists()
        return False