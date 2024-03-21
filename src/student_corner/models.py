from django.db import models


class CourseRegistration(models.Model):
    student_account = models.ForeignKey(
        "account.User", on_delete=models.CASCADE, related_name="student_account"
    )
    enrolled_in = models.ForeignKey(
        "course.Course", on_delete=models.CASCADE, related_name="enrolled_in"
    )
    fee_paid = models.FloatField()
    is_registered = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
