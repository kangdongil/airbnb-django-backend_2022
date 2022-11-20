from datetime import timedelta
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
    event_duration = models.DurationField(
        default=timedelta(hours=2),
    )
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

    @property
    def total_reviews(experience):
        return experience.reviews.count()

    def average_ratings(experience):
        reviews = experience.reviews.count()
        if reviews == 0:
            return 0
        else:
            total_ratings = 0
            for review in experience.reviews.all().values("rating"):
                total_ratings += review["rating"]
            return round(total_ratings / reviews, 2)

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