from rest_framework.serializers import ModelSerializer
from .models import Wishlist
from rooms.serializers import WishlistRoomSerializer
from experiences.serializers import WishlistExperienceSerializer


class WishlistSerializer(ModelSerializer):
    
    rooms = WishlistRoomSerializer(
        many=True,
        read_only=True,
    )
    experiences = WishlistExperienceSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Wishlist
        fields = (
            "pk",
            "name",
            "rooms",
            "experiences",
        )