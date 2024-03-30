from django.db import models
from course.models import Course
from review.utils import RatingChoice


class Review(models.Model):
    account = models.ForeignKey("account.User", on_delete=models.CASCADE)
    course = models.ForeignKey("course.Course", on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.FloatField(choices=RatingChoice.choices, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    indexes = [
        models.Index(fields=["course"]),
    ]
