from django.db import models
from common.models import TimeStampedModel

class Review(TimeStampedModel):

    """ Review Model Definition """

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    room = models.ForeignKey(
        "rooms.Room",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="reviews",
    )
    experience = models.ForeignKey(
       "experiences.Experience",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="reviews",
    )
    payload = models.TextField(null=True, blank=True)
    rating = models.PositiveIntegerField()

    def category(review):
        if review.room and not review.experience:
            return "Room"
        elif not review.room and review.experience:
            return "Experience"

    def target_name(review):
        if review.room and not review.experience:
            return f"{review.room}"
        elif not review.room and review.experience:
            return f"{review.experience}"
            
    def __str__(review):
        return f"{review.user} / ★{review.rating}"