from django.db import models


class ApplicationStatusEnum(models.TextChoices):
    ACCEPTED = "accepted"
    PENDING = "pending"
    REJECTED = "rejected"
