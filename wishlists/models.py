from django.db import models
from common.models import TimeStampedModel


class Wishlist(TimeStampedModel):

    """ Wishlist Model Definition """

    name = models.CharField(max_length=150)
    rooms = models.ManyToManyField(
        "rooms.Room",
        blank=True,
        related_name="wishlists",
    )
    experiences = models.ManyToManyField(
        "experiences.Experience",
        blank=True,
        related_name="wishlists",
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="wishlists",
    )

    def __str__(self):
        return self.name