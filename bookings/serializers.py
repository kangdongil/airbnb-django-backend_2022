from rest_framework.serializers import ModelSerializer
from .models import Booking


class PublicBookingSerializer(ModelSerializer):
    class Meta:
        model=Booking
        fields = (
            "pk",
            "check_in",
            "check_out",
            "experience_time",
        )