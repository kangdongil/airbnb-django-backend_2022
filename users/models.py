from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male")
        FEMALE = ("female", "Female")
        HIDDEN = ("hidden", "Rather not say")

    class LanguageChoices(models.TextChoices):
        KR = ("kr", "Korean")
        EN = ("en", "English")
        JP = ("jp", "Japanese")
        ES = ("es", "Espanol")
        FR = ("fr", "French")

    class CurrencyChoices(models.TextChoices):
        WON = ("won", "Korean Won")
        USD = ("usd", "US Dollar")
        JPY = ("jpy", "Japanese Yen")
        EUR = ("eur", "Euro")

    name = models.CharField(max_length=150, default="")
    first_name = models.CharField(
        max_length=150,
        editable=False,
    )
    last_name = models.CharField(
        max_length=150,
        editable=False,
    )
    avatar = models.ImageField(blank=True)
    is_host = models.BooleanField(default=False)
    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,
        default=GenderChoices.HIDDEN,
    )
    language = models.CharField(
        max_length=3,
        choices=LanguageChoices.choices,
        default=LanguageChoices.KR,
    )
    currency = models.CharField(
        max_length=5,
        choices=CurrencyChoices.choices,
        default=CurrencyChoices.WON,
    )

