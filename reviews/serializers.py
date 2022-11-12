from rest_framework.serializers import ModelSerializer
from .models import Review
from common.serializers import TinyUserSerializer
from common.serializers import TinyRoomSerializer
from bookings.serializers import PublicBookingSerializer


class UserReviewSerializer(ModelSerializer):
    
    class Meta:
        model=Review
        fields = (
            "payload",
            "rating",
            "created_at",
        )


class HostReviewSerializer(ModelSerializer):
    
    user = TinyUserSerializer(read_only=True)
    room = TinyRoomSerializer(read_only=True)

    class Meta:
        model=Review
        fields = (
            "user",
            "room",
            "payload",
            "rating",
            "created_at",
        )


class ReviewSerializer(ModelSerializer):
    
    user = TinyUserSerializer(read_only=True)
    booking = PublicBookingSerializer(read_only=True)

    class Meta:
        model=Review
        fields = (
            "user",
            "booking",
            "payload",
            "rating",
            "created_at",
        )