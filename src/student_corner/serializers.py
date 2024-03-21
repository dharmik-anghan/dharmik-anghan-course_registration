from rest_framework import serializers

from student_corner.models import CourseRegistration


class RegisterForCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseRegistration
        fields = ["student_account", "enrolled_in"]
