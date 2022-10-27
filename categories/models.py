from django.db import models
from common.models import TimeStampedModel

class Category(TimeStampedModel):

    """ Room or Experience Category Model Defintion """

    class CategoryKindChoices(models.TextChoices):
        ROOM = ("rooms", "Rooms")
        EXPERIENCE = ("experiences", "Experiences")

    name = models.CharField(max_length=50)
    kind = models.CharField(
        max_length=20,
        choices=CategoryKindChoices.choices,
    )

    def __str__(self):
        return f"{self.kind.title()}: {self.name}"

    class Meta:
        verbose_name_plural = "Categories"