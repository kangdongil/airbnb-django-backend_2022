from django.db import models
from common.models import TimeStampedModel


class Booking(TimeStampedModel):

    """ Booking Model Definition """

    class BookingKindChoices(models.TextChoices):

        ROOM = ("room", "Room")
        EXPERIENCE = ("experience", "Experience")

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

    def __str__(self):
        return f"{self.kind.title()} booking for: {self.user}"
    
    def place(booking):
        if booking.room:
            return f"room: {booking.room}"
        elif booking.experience:
            return f"experience: {booking.experience}"
        else:
            return None