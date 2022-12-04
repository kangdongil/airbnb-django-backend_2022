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
        related_name="rooms"
    )
    amenities = models.ManyToManyField(
        "Amenity",
        related_name="rooms",
    )
    category = models.ForeignKey(
        "categories.Category",
        on_delete=models.SET_NULL,
        related_name="rooms",
        null=True,
        blank=True,
    )
    pet_friendly = models.BooleanField(
        default=False,
    )

    def total_reviews(room):
        return room.reviews.count()

    def average_ratings(room):
        reviews = room.reviews.count()
        if reviews == 0:
            return 0
        else:
            total_ratings = 0
            for review in room.reviews.all().values("rating"):
                total_ratings += review["rating"]
            return round(total_ratings / reviews, 2)

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