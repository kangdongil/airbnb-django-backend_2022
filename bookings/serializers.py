from django.utils import timezone
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Booking
from common.serializers import TinyUserSerializer


class PublicBookingSerializer(ModelSerializer):
    class Meta:
        model=Booking
        fields = (
            "pk",
            "check_in",
            "check_out",
            "experience_time",
        )


class PrivateBookingSerializer(ModelSerializer):

    user = TinyUserSerializer(read_only=True)
    booking_state = SerializerMethodField()

    class Meta:
        model=Booking
        fields = (
            "pk",
            "user",
            "check_in",
            "check_out",
            "experience_time",
            "guests",
            "booking_state",
            "is_cancelled",
        )

    def get_booking_state(self, booking):
        return booking.booking_state


class CreateRoomBookingSerializer(ModelSerializer):
    
    check_in = serializers.DateField()
    check_out = serializers.DateField()

    class Meta:
        model=Booking
        fields = (
            "check_in",
            "check_out",
            "guests",
        )
    
    def validate_check_in(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't book in the past!")
        return value

    def validate_check_out(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't book in the past!")
        return value
    
    def validate(self, data):
        if data['check_out'] <= data['check_in']:
            raise serializers.ValidationError("Check-in should be older than check-out.")
        if Booking.objects.filter(
            check_in__lte = data["check_out"],
            check_out__gte = data["check_in"],
        ).exists():
            raise serializers.ValidationError("Those Dates are already taken.")
        return data