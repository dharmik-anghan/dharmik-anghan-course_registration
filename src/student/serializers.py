from rest_framework import serializers

from student.models import CoursePurchase


class RegisterForCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoursePurchase
        fields = ["student", "course"]
