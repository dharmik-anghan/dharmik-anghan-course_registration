from django.contrib import admin
from instructor.models import Instructor


class InsstructorAdmin(admin.ModelAdmin):
    model = Instructor

    list_display = [
        "instructor",
        "get_instructor_first_name",
        "get_qualification_education",
        "course_count",
        "money_earned",
        "created_at",
        "application_status",
        "accepted_by",
        "is_deleted",
    ]

    list_editable = ["is_deleted", "application_status"]

    search_fields = ["instructor__first_name"]

    def get_instructor_first_name(self, obj):
        return obj.instructor.first_name

    get_instructor_first_name.short_description = "Instructor First Name"

    def get_qualification_education(self, obj):
        return obj.qualification.education

    get_qualification_education.short_description = "Qualification Education"


admin.site.register(Instructor, InsstructorAdmin)
