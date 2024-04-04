from django.contrib import admin
from student.models import CoursePurchase


class CoursePurchaseAdmin(admin.ModelAdmin):
    model = CoursePurchase

    list_display = [
        "student",
        "get_student_first_name",
        "course",
        "fees_paid",
        "is_registered",
        "created_at",
    ]

    list_editable = ["is_registered"]

    def get_student_first_name(self, obj):
        return obj.student.first_name

    get_student_first_name.short_description = "Student First Name"


admin.site.register(CoursePurchase, CoursePurchaseAdmin)
