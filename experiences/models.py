from django.db import models
from common.models import TimeStampedModel


class Experience(TimeStampedModel):

    """ Experience Model Definition """

    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    price = models.PositiveIntegerField()
    event_start = models.TimeField()
    event_end = models.TimeField()
    host = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        related_name="experiences",
        null=True,
        blank=True,
    )
    perks = models.ManyToManyField(
        "Perk",
        related_name="experiences",
    )
    category = models.ForeignKey(
        "categories.Category",
        on_delete=models.SET_NULL,
        related_name="experiences",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class Perk(TimeStampedModel):

    """ Perk Model Definitioin """

    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    details = models.CharField(
        max_length=250,
        blank=True,
        default="",
    )

    def __str__(self):
        return self.name