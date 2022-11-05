from django.db import models
from common.models import TimeStampedModel


class Photo(TimeStampedModel):

    """ Photo Model Definition """

    file = models.URLField()
    description = models.CharField(max_length=250, default="")
    room = models.ForeignKey(
        "rooms.Room",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="photos",
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="photos",
    )

    def __str__(self):
        return "Photo File"


class Video(TimeStampedModel):

    """ Video Model Definition """

    file = models.URLField()
    description = models.CharField(max_length=250, default="")
    experience = models.ForeignKey(
        "experiences.Experience",
        on_delete=models.CASCADE,
        related_name="videos",
    )

    def __str__(self):
        return "Video File"