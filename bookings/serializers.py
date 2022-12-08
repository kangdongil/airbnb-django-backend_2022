from datetime import datetime, date, timedelta
from django.utils import timezone
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Booking
from common.serializers import TinyUserSerializer
from experiences.models import Experience


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
        room = self.context.get("room")
        if data['check_out'] <= data['check_in']:
            raise serializers.ValidationError("Check-in should be older than check-out.")
        if Booking.objects.filter(
            room=room,
            check_in__lte = data["check_out"],
            check_out__gte = data["check_in"],
        ).exists():
            raise serializers.ValidationError("Those Dates are already taken.")
        return data


class CreateExperienceBookingSerializer(ModelSerializer):

    experience_time = serializers.DateTimeField()

    class Meta:
        model = Booking
        fields = (
            "experience_time",
            "guests",
        )

    def apply_date_to_time(self, date, time):
        datetime_utc = timezone.make_aware(
            datetime.combine(
                timezone.make_naive(date, timezone=timezone.utc),
                time,
            ),
            timezone=timezone.utc,
        )
        return timezone.localtime(datetime_utc)

    def validate_experience_time(self, value):
        now = timezone.localtime(timezone.now())
        event_start_time = self.context["experience"].event_start
        event_end_time = self.context["experience"].event_end

        event_start = self.apply_date_to_time(
            value,
            event_start_time,
        )
        if event_start_time <= event_end_time:
            event_end = self.apply_date_to_time(
                value,
                event_end_time,
            )
        elif event_start_time > event_end_time:
            event_end = self.apply_date_to_time(
                value,
                event_end_time,
            ) + timedelta(days=1)
        
        if now > value:
            raise serializers.ValidationError("Can't book in the past!")
        elif value < event_start:
            raise serializers.ValidationError(f"Event hasn't open yet. Book after {event_start.time()}")
        elif value >= event_end:
            raise serializers.ValidationError("Event closed. Try tomorrow.")
        if Booking.objects.filter(
            experience_time__lt = value + self.context["experience"].event_duration,
            experience_time__gt = value - self.context["experience"].event_duration,
        ).exists():
            raise serializers.ValidationError("Those times are already taken.")
        return value