from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Experience, Perk
from common.serializers import TinyUserSerializer
from wishlists.models import Wishlist
from medias.models import Photo
from categories.serializers import CategorySerializer
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer, VideoSerializer

class PerkSerializer(ModelSerializer):
    class Meta:
        model = Perk
        fields = "__all__"


class WishlistExperienceSerializer(ModelSerializer):
    
    photos = PhotoSerializer(
        read_only=True,
        many=True,
    )
    is_liked = SerializerMethodField()

    class Meta:
        model = Experience
        fields = (
            "pk",
            "name",
            "price",
            "photos",
            "is_liked",
        )
    
    def get_is_liked(self, experience):
        request = self.context["request"]
        return Wishlist.objects.filter(
            owner=request.user,
            experiences__pk=experience.pk,
        ).exists()


class HostExperienceSerializer(ModelSerializer):

    preview_photo = SerializerMethodField()
    rating = SerializerMethodField()
    total_reviews = SerializerMethodField()

    class Meta:
        model=Experience
        fields=(
            "pk",
            "name",
            "preview_photo",
            "rating",
            "total_reviews",
        )
    
    def get_rating(self, experience):
        return experience.average_ratings()
    
    def get_total_reviews(self, experience):
        return experience.total_reviews

    def get_preview_photo(self, experience):
        try:
            preview_photo = Photo.objects.get(
                experience=experience,
                is_thumbnail=True,
            )
        except Photo.DoesNotExist:
            return
        return PhotoSerializer(preview_photo).data

class ExperienceListSerializer(ModelSerializer):

    
    photos = PhotoSerializer(
        read_only=True,
        many=True,
    )
    video = VideoSerializer(
        read_only=True,
    )
    rating = SerializerMethodField()
    is_owner = SerializerMethodField()
    is_liked = SerializerMethodField()

    class Meta:
        model = Experience
        fields = (
            "pk",
            "name",
            "photos",
            "video",
            "country",
            "city",
            "price",
            "rating",
            "is_owner",
            "is_liked",
        )

    def get_rating(self, experience):
        return experience.average_ratings()

    def get_is_owner(self, experience):
        request = self.context["request"]
        return experience.host == request.user

    def get_is_liked(self, experience):
        request = self.context["request"]
        return Wishlist.objects.filter(
            owner=request.user,
            experiences__pk=experience.pk,
        ).exists()


class ExperienceDetailSerializer(ModelSerializer):

    host = TinyUserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    perks = PerkSerializer(
        read_only=True,
        many=True,
    )
    reviews = ReviewSerializer(
        read_only=True,
        many=True,
    )
    photos = PhotoSerializer(
        read_only=True,
        many=True,
    )
    video = VideoSerializer(
        read_only=True,
    )
    rating = SerializerMethodField()
    is_host = SerializerMethodField()
    is_liked = SerializerMethodField()

    class Meta:
        model = Experience
        fields = (
            "pk",
            "name",
            "description",
            "country",
            "city",
            "address",
            "rating",
            "price",
            "is_liked",
            "event_start",
            "event_end",
            "event_duration",
            "is_host",
            "host",
            "category",
            "photos",
            "video",
            "perks",
            "reviews",
            "created_at",
            "updated_at",
        )

    def get_rating(self, experience):
        return experience.average_ratings()

    def get_is_host(self, experience):
        request = self.context["request"]
        return experience.host == request.user

    def get_is_liked(self, experience):
        request = self.context["request"]
        return Wishlist.objects.filter(
            owner=request.user,
            experiences__pk=experience.pk,
        ).exists()