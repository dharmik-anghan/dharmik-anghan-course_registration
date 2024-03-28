from datetime import datetime
from django.db import models
from course.utils import CourseLevelStatusEnum, CourseStatusEnum
from instructor.models import Instructor


def upload_image(instance, filename):
    name, ext = filename.rsplit(".")
    filename = str(datetime.now().timestamp()).split(".")[0] + "." + ext
    upload_path = f"uploads/{instance.instructor.id}/{filename}"
    return upload_path


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Course(models.Model):
    instructor = models.ForeignKey("instructor.Instructor", on_delete=models.CASCADE)
    course_name = models.CharField(max_length=255)
    course_description = models.TextField()
    course_duration = models.TimeField()
    course_price = models.FloatField()
    student_count = models.IntegerField(default=0)
    rating = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    categories = models.ForeignKey(
        "course.Category", related_name="courses", blank=True, on_delete=models.CASCADE
    )
    course_image = models.ImageField(upload_to=upload_image, blank=True, null=True)
    prerequisites = models.TextField(blank=True)
    course_outline = models.TextField(blank=True)
    course_status = models.CharField(
        max_length=20, choices=CourseStatusEnum.choices, default="upcoming"
    )
    level = models.CharField(
        max_length=20,
        choices=CourseLevelStatusEnum.choices,
        blank=True,
    )
    language = models.CharField(max_length=50, blank=True)
    discounts = models.FloatField(default=0.0)

    def __str__(self):
        return self.course_name
