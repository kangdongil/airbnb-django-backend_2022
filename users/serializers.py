from django.db.models import Avg, Count
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import User
from reviews.models import Review
from reviews.serializers import UserReviewSerializer, HostReviewSerializer
from rooms.models import Room
from rooms.serializers import HostRoomSerializer
from experiences.models import Experience
from experiences.serializers import HostExperienceSerializer

class PrivateUserSerializer(ModelSerializer):
    class Meta:
        model=User
        """
        exclude=(
            "id",
            "password",
            "is_superuser",
            "is_staff",
            "is_active",
            "first_name",
            "last_name",
            "groups",
            "user_permissions",
        )
        """
        fields=(
            "username",
            "email",
            "avatar",
            "name",
            "last_login",
            "date_joined",
            "is_host",
            "gender",
            "language",
            "currency",
        )


class PublicUserSerializer(ModelSerializer):

    reviews = SerializerMethodField()
    rooms = SerializerMethodField()
    experiences = SerializerMethodField()
    host_reviews = SerializerMethodField()

    class Meta:
        model=User
        fields=(
            "username",
            "email",
            "avatar",
            "name",
            "last_login",
            "date_joined",
            "reviews",
            "is_host",
            "rooms",
            "experiences",
            "host_reviews",
            "gender",
            "language",
            "currency",
        )
    
    def get_reviews(self, user):
        recent_reviews = Review.objects.filter(user=user)\
            .order_by("-created_at")[:10]
        return UserReviewSerializer(recent_reviews, many=True).data
    
    def get_rooms(self, owner):
        query_exp = {
            "cnt_reviews": Count("reviews"),
            "avg_ratings": Avg("reviews__rating"),
        }
        ordering = ["-cnt_reviews", "-avg_ratings"]
        owned_rooms = Room.objects.filter(owner=owner)\
            .annotate(**query_exp).order_by(*ordering)[:10]
        return HostRoomSerializer(owned_rooms, many=True).data

    def get_experiences(self, host):
        query_exp = {
            "cnt_reviews": Count("reviews"),
            "avg_ratings": Avg("reviews__rating"),
        }
        ordering = ["-cnt_reviews", "-avg_ratings"]
        hosted_experiences = Experience.objects.filter(host=host)\
            .annotate(**query_exp).order_by(*ordering)[:10]
        return HostExperienceSerializer(hosted_experiences, many=True).data

    def get_host_reviews(self, owner):
        reviews = Review.objects.filter(room__owner=owner)[:10]
        return HostReviewSerializer(reviews, many=True).data