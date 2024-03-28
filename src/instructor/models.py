from django.db import models
from instructor.utils import ApplicationStatusEnum


class Qualification(models.Model):
    education = models.CharField(max_length=100, unique=True, null=False)


class Instructor(models.Model):
    instructor = models.OneToOneField(
        "account.User", on_delete=models.CASCADE, related_name="instructor", unique=True
    )
    qualification = models.ForeignKey(
        "instructor.Qualification",
        on_delete=models.CASCADE,
        related_name="qualification",
        blank=True,
        null=True,
    )
    description = models.TextField()
    course_count = models.PositiveIntegerField(default=0)
    money_earned = models.PositiveBigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    application_status = models.CharField(
        max_length=15,
        choices=ApplicationStatusEnum.choices,
        default=ApplicationStatusEnum.PENDING,
    )
    reason_for_rejection = models.TextField(null=True, blank=True)
    accepted_by = models.ForeignKey(
        "account.User",
        on_delete=models.CASCADE,
        related_name="accepted_instructors",
        null=True,
        blank=True,
    )
    accepted_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
