from django.db import models


class Course(models.Model):
    tutor = models.ForeignKey("tutor_account.Tutor", on_delete=models.CASCADE)
    course_name = models.CharField(max_length=255)
    course_description = models.TextField()
    course_duration = models.TimeField()
    course_price = models.FloatField()
    student_count = models.IntegerField(default=0)
    rating = models.FloatField(default=0.0)
    url = models.URLField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
