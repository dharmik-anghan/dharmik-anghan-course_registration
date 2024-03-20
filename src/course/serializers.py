from course.models import Course
from rest_framework import serializers


class CourseTutorRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            "tutor",
            "course_name",
            "course_description",
            "course_duration",
            "course_price",
            "url",
        ]


class CourseDetailsSerializer(serializers.ModelSerializer):
    def getTutorName(self, obj):
        return obj.tutor.account.first_name

    def getTutorDesc(self, obj):
        return obj.tutor.description

    def getTutorQuali(self, obj):
        return obj.tutor.qualification

    tutor_name = serializers.SerializerMethodField("getTutorName")
    tutor_description = serializers.SerializerMethodField("getTutorDesc")
    tutor_qualification = serializers.SerializerMethodField("getTutorQuali")

    class Meta:
        model = Course
        fields = [
            "course_name",
            "course_description",
            "course_duration",
            "course_price",
            "created_at",
            "tutor",
            "tutor_name",
            "tutor_description",
            "tutor_qualification",
        ]
