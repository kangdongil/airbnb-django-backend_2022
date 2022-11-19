from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Experience
from common.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer


class ExperienceListSerializer(ModelSerializer):

    rating = SerializerMethodField()
    is_owner = SerializerMethodField()

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
        )

    def get_rating(self, experience):
        return experience.average_ratings()

    def get_is_owner(self, experience):
        request = self.context["request"]
        return experience.host == request.user


class ExperienceDetailSerializer(ModelSerializer):

    host = TinyUserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    # perk
    # reviews
    # photos
    # video
    rating = SerializerMethodField()
    is_host = SerializerMethodField()

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
            "event_start",
            "event_end",
            "is_host",
            "host",
            "category",
            "perks",
            "created_at",
            "updated_at",
        )

    def get_rating(self, experience):
        return experience.average_ratings()

    def get_is_host(self, experience):
        request = self.context["request"]
        return experience.host == request.user