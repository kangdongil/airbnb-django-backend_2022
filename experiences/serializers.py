from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Experience, Perk
from common.serializers import TinyUserSerializer
from wishlists.models import Wishlist
from categories.serializers import CategorySerializer
from reviews.serializers import ReviewSerializer


class PerkSerializer(ModelSerializer):
    class Meta:
        model = Perk
        fields = "__all__"


class WishlistExperienceSerializer(ModelSerializer):
    
    is_liked = SerializerMethodField()

    class Meta:
        model = Experience
        fields = (
            "pk",
            "name",
            "price",
            "is_liked",
        )
    
    def get_is_liked(self, experience):
        request = self.context["request"]
        return Wishlist.objects.filter(
            owner=request.user,
            experiences__pk=experience.pk,
        ).exists()


class HostExperienceSerializer(ModelSerializer):

    rating = SerializerMethodField()
    total_reviews = SerializerMethodField()

    class Meta:
        model=Experience
        fields=(
            "pk",
            "name",
            "rating",
            "total_reviews",
        )
    
    def get_rating(self, experience):
        return experience.average_ratings()
    
    def get_total_reviews(self, experience):
        return experience.total_reviews


class ExperienceListSerializer(ModelSerializer):

    rating = SerializerMethodField()
    is_owner = SerializerMethodField()
    is_liked = SerializerMethodField()

    class Meta:
        model = Experience
        fields = (
            "pk",
            "name",
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
    # photos
    # video
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