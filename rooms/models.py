from django.db import models
from common.models import TimeStampedModel


class Room(TimeStampedModel):

    """ Room Model Definition """

    class RoomKindChoices(models.TextChoices):
        ENTIRE_PLACE = ("entire place", "Entire Place")
        PRIVATE_ROOM = ("private room", "Private Room")
        SHARED_ROOM = ("shared room", "Shared Room")

    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    country = models.CharField(max_length=50, default="South Korea")
    city = models.CharField(max_length=50, default="Seoul")
    address = models.CharField(max_length=250)
    price = models.PositiveIntegerField()
    rooms = models.PositiveIntegerField()
    toilets = models.PositiveIntegerField()
    kind = models.CharField(
        max_length=25,
        choices=RoomKindChoices.choices,
        default=RoomKindChoices.ENTIRE_PLACE,
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
    amenities = models.ManyToManyField("Amenity")

    def __str__(self):
        return self.name

class Amenity(TimeStampedModel):

    """ Amenity Model Definition """

    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Amenities"