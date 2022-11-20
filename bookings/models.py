from datetime import datetime
from django.db import models
from django.utils import timezone
from common.models import TimeStampedModel


class Booking(TimeStampedModel):

    """ Booking Model Definition """

    class BookingKindChoices(models.TextChoices):

        ROOM = ("room", "Room")
        EXPERIENCE = ("experience", "Experience")

    class BookingHostApprovalChoices(models.TextChoices):

        PENDING = ("pending", "Pending")
        CONFIRMED = ("confirmed", "Confirmed")
        DENIED = ("denied", "Denied")

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    kind = models.CharField(
        max_length=15,
        choices=BookingKindChoices.choices,
    )
    room = models.ForeignKey(
        "rooms.Room",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bookings"
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bookings",
    )
    check_in = models.DateField(
        null=True,
        blank=True,
    )
    check_out = models.DateField(
        null=True,
        blank=True,
    )
    experience_time = models.DateTimeField(
        null=True,
        blank=True,
    )
    guests = models.PositiveIntegerField()
    is_cancelled = models.BooleanField(
        default=False,
    )
    host_approval_state = models.CharField(
        max_length=15,
        choices=BookingHostApprovalChoices.choices,
        default=BookingHostApprovalChoices.PENDING,
    )

    def __str__(self):
        if self.check_in and self.check_out:
            check_in_date = datetime.strftime(self.check_in, "%y%m%d")
            check_out_date = datetime.strftime(self.check_out, "%m%d")
            booking_date = f"{check_in_date}{check_out_date}"
        elif self.experience_time:
            booking_date = datetime.strftime(self.experience_time, "%y%m%d%H%M")
        return f"{booking_date}-{self.user}-{self.event_name}"
    
    @property
    def event_name(booking):
        if booking.room:
            return booking.room
        elif booking.experience:
            return booking.experience
        else:
            return None

    @property
    def booking_state(booking):
        now = timezone.localtime(timezone.now())
        if booking.is_cancelled:
            return "cancelled"
        if (booking.check_in and now.date() > booking.check_in) or (
            booking.experience_time and now > booking.experience_time
        ):
            if not booking.host_approval_state == "confirmed":
                return "denied"
            return "finished"
        return booking.host_approval_state
