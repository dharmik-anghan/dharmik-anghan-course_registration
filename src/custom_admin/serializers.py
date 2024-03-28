from rest_framework import serializers

from course.models import Category
from instructor.models import Qualification, Instructor
from instructor.utils import ApplicationStatusEnum


class AddQualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualification
        fields = ["education"]

    def create(self, validated_data):
        return Qualification.objects.create(**validated_data)


class InstructorSerializer(serializers.ModelSerializer):
    instructor_email = serializers.CharField(source="instructor.email", read_only=True)
    qualification_education = serializers.CharField(
        source="qualification.education", read_only=True
    )
    accepted_by_email = serializers.CharField(
        source="accepted_by.email", read_only=True
    )

    class Meta:
        model = Instructor
        fields = [
            "instructor",
            "instructor_email",
            "qualification_education",
            "description",
            "course_count",
            "money_earned",
            "created_at",
            "updated_at",
            "application_status",
            "reason_for_rejection",
            "accepted_at",
            "accepted_by",
            "accepted_by_email",
            "accepted_at",
        ]


class UpdateStatusofApplicationSerializer(serializers.ModelSerializer):
    instructor_id = serializers.IntegerField()
    reason_for_rejection = serializers.CharField(required=False)

    class Meta:
        model = Instructor
        fields = ["instructor_id", "application_status", "reason_for_rejection"]

    def validate(self, attrs):

        if (
            attrs.get("application_status") == ApplicationStatusEnum.REJECTED
            or attrs.get("application_status") == ApplicationStatusEnum.PENDING
        ):
            if attrs.get("reason_for_rejection") is None:
                raise Exception("'reason_for_rejection' field required")

        return attrs


class CourseCategoryserializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]
