from course.models import Course
from rest_framework import serializers

from student_corner.models import CourseRegistration


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

    def getHasEnrolled(self, obj):
        request = self.context.get("request")
        user_id = request.user.id
        registration = CourseRegistration.objects.filter(
            enrolled_in=obj.id, student_account=user_id
        ).first()
        if registration:
            if registration.is_registered:
                return True
        return False

    tutor_name = serializers.SerializerMethodField("getTutorName")
    tutor_description = serializers.SerializerMethodField("getTutorDesc")
    tutor_qualification = serializers.SerializerMethodField("getTutorQuali")
    has_enrolled = serializers.SerializerMethodField("getHasEnrolled")

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
            "student_count",
            "has_enrolled",
        ]


class FullDetailsforEnrolledSerializer(serializers.ModelSerializer):
    def getTutorName(self, obj):
        return obj.tutor.account.first_name

    def getTutorDesc(self, obj):
        return obj.tutor.description

    def getTutorQuali(self, obj):
        return obj.tutor.qualification

    def getHasEnrolled(self, obj):
        request = self.context.get("request")
        user_id = request.user.id
        registration = CourseRegistration.objects.filter(
            enrolled_in=obj.id, student_account=user_id
        ).first()
        if registration:
            if registration.is_registered:
                return True
        return False

    tutor_name = serializers.SerializerMethodField("getTutorName")
    tutor_description = serializers.SerializerMethodField("getTutorDesc")
    tutor_qualification = serializers.SerializerMethodField("getTutorQuali")
    has_enrolled = serializers.SerializerMethodField("getHasEnrolled")

    class Meta:
        model = Course
        fields = [
            "course_name",
            "url",
            "course_description",
            "course_duration",
            "course_price",
            "created_at",
            "tutor",
            "tutor_name",
            "tutor_description",
            "tutor_qualification",
            "student_count",
            "has_enrolled",
        ]
