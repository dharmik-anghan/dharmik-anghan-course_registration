from django.db import models
from django.core.validators import MinValueValidator


class CoursePurchase(models.Model):
    student = models.ForeignKey(
        "account.User", on_delete=models.CASCADE, related_name="course_purchases"
    )
    course = models.ForeignKey(
        "course.Course", on_delete=models.CASCADE, related_name="course_purchases"
    )
    fees_paid = models.FloatField(validators=[MinValueValidator(0)])
    is_registered = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    indexes = [
        models.Index(fields=["student"]),
    ]
