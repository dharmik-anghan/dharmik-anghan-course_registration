from django.contrib import admin

from course.models import Course


class CourseAdmin(admin.ModelAdmin):
    model = Course

    list_display = [
        "id",
        "tutor",
        "course_name",
        "course_price",
        "created_at",
        "course_duration",
        "is_deleted",
    ]

    list_editable = ["is_deleted"]

    list_filter = ["course_price", "created_at", "course_duration"]


admin.site.register(Course, CourseAdmin)
