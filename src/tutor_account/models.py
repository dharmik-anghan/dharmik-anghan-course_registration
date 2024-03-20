from django.db import models

APPLICATION_STATUS = (
    ("accepted", "accepted"),
    ("pending", "pending"),
    ("rejected", "rejected"),
)


class Tutor(models.Model):
    account = models.OneToOneField(
        "account.User", on_delete=models.CASCADE, related_name="tutor", unique=True
    )
    qualification = models.CharField(max_length=255)
    description = models.TextField()
    course_count = models.PositiveIntegerField(default=0)
    money_earned = models.PositiveBigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    application_accepted = models.BooleanField(default=False)
    application_status = models.CharField(
        max_length=15, default="pending", choices=APPLICATION_STATUS
    )
    reason_for_rejection = models.TextField(null=True, blank=True)
    application_accepted_by = models.ForeignKey(
        "account.User",
        on_delete=models.CASCADE,
        related_name="admin",
        null=True,
        blank=True,
        unique=False,
    )
    accepted_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
