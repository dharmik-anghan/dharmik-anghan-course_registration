from django.db import models


class RatingChoice(models.TextChoices):
    ONE = 1.0
    ONEHALF = 1.5
    TWO = 2.0
    TWOHALF = 2.5
    THREE = 3.0
    THREEHALF = 3.5
    FOUR = 4.0
    FOURHALF = 4.5
    FIVE = 5.0
