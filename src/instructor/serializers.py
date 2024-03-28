from instructor.models import Instructor, Qualification
from rest_framework import serializers


class InstructorSerializer(serializers.ModelSerializer):
    instructor_email = serializers.CharField(source="instructor.email", read_only=True)
    qualification_education = serializers.CharField(
        source="qualification.education", read_only=True
    )

    class Meta:
        model = Instructor
        fields = [
            "instructor_email",
            "qualification_education",
            "description",
            "course_count",
            "money_earned",
            "created_at",
            "application_status",
            "reason_for_rejection",
            "accepted_at",
        ]


class RegisterForInstructorSerializer(serializers.ModelSerializer):
    id = serializers.Serializer(read_only=True)

    class Meta:
        model = Instructor
        fields = [
            "id",
            "qualification",
            "description",
        ]

    def validate(self, attrs):
        try:
            Qualification.objects.get(pk=attrs.get("qualification").id)
        except Qualification.DoesNotExist:
            return Exception("Qualificatoin not found")
        return attrs


class CourseInstructorSerializer(serializers.ModelSerializer):
    instructor_email = serializers.CharField(source="instructor.email", read_only=True)
    qualification_education = serializers.CharField(
        source="qualification.education", read_only=True
    )
    first_name = serializers.CharField(source="instructor.first_name", read_only=True)
    last_name = serializers.CharField(source="instructor.last_name", read_only=True)

    class Meta:
        model = Instructor
        fields = [
            "id",
            "first_name",
            "last_name",
            "instructor_email",
            "qualification_education",
            "description",
            "course_count",
            "created_at",
        ]
