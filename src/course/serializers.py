from course.models import Category, Course
from rest_framework import serializers
from instructor.models import Instructor
from instructor.serializers import CourseInstructorSerializer
from student.models import CoursePurchase


class GetCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class GetCourseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)
    course_image = serializers.ImageField(
        allow_empty_file=False, use_url=False, write_only=True
    )

    class Meta:
        model = Course
        fields = [
            "id",
            "instructor",
            "course_name",
            "course_description",
            "course_duration",
            "course_price",
            "categories",
            "course_image",
            "prerequisites",
            "course_outline",
            "course_status",
            "level",
            "language",
            "discounts",
            "image",
            "created_at",
            "updated_at",
            "student_count",
            "rating",
        ]

    def get_image(self, obj):
        request = self.context.get("request")
        image = obj.course_image.url
        return request.build_absolute_uri(image)


class RegisterCourseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)
    course_image = serializers.ImageField(
        allow_empty_file=False, use_url=False, write_only=True
    )

    class Meta:
        model = Course
        fields = [
            "id",
            "instructor",
            "course_name",
            "course_description",
            "course_duration",
            "course_price",
            "categories",
            "course_image",
            "prerequisites",
            "course_outline",
            "course_status",
            "level",
            "language",
            "discounts",
            "image",
        ]

    def get_image(self, obj):
        request = self.context.get("request")
        image = obj.course_image.url
        return request.build_absolute_uri(image)


class UploadCourseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)
    course_image = serializers.ImageField(
        allow_empty_file=False, use_url=False, write_only=True
    )

    class Meta:
        model = Course
        fields = [
            "id",
            "course_name",
            "course_description",
            "course_duration",
            "course_price",
            "categories",
            "course_image",
            "prerequisites",
            "course_outline",
            "course_status",
            "level",
            "language",
            "discounts",
            "image",
        ]

    def get_image(self, obj):
        request = self.context.get("request")
        image = obj.course_image.url
        return request.build_absolute_uri(image)


# class CourseDetailsSerializer(serializers.ModelSerializer):
#     def getTutorName(self, obj):
#         return obj.tutor.account.first_name

#     def getTutorDesc(self, obj):
#         return obj.tutor.description

#     def getTutorQuali(self, obj):
#         return obj.tutor.qualification

#     def getHasEnrolled(self, obj):
#         request = self.context.get("request")
#         user_id = request.user.id
#         registration = CourseRegistration.objects.filter(
#             enrolled_in=obj.id, student_account=user_id
#         ).first()
#         if registration:
#             if registration.is_registered:
#                 return True
#         return False

#     tutor_name = serializers.SerializerMethodField("getTutorName")
#     tutor_description = serializers.SerializerMethodField("getTutorDesc")
#     tutor_qualification = serializers.SerializerMethodField("getTutorQuali")
#     has_enrolled = serializers.SerializerMethodField("getHasEnrolled")

#     class Meta:
#         model = Course
#         fields = [
#             "course_name",
#             "course_description",
#             "course_duration",
#             "course_price",
#             "created_at",
#             "tutor",
#             "tutor_name",
#             "tutor_description",
#             "tutor_qualification",
#             "student_count",
#             "has_enrolled",
#         ]


class InstructorandCourseDetailsSerializer(serializers.ModelSerializer):
    def get_final_price(self, obj):
        course_price = obj.course_price
        discounts = obj.discounts

        # Calculate the final price after applying discounts
        final_price = course_price - (course_price * discounts * 0.01)

        return final_price

    def get_instructor(self, obj):
        instructor_id = obj.instructor.id
        instructor = Instructor.objects.get(id=instructor_id)
        serializer = CourseInstructorSerializer(instructor)
        return serializer.data

    def get_has_enrolled(self, obj):
        request = self.context.get("request")
        user_id = request.user.id
        registration = CoursePurchase.objects.filter(
            course=obj.id, student=user_id
        ).first()
        if registration:
            if registration.is_registered:
                return True
        return False

    def get_image(self, obj):
        request = self.context.get("request")
        image = obj.course_image.url
        return request.build_absolute_uri(image)

    instructor = serializers.SerializerMethodField("get_instructor")
    has_enrolled = serializers.SerializerMethodField("get_has_enrolled")
    final_price = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = [
            "id",
            "course_name",
            "course_description",
            "course_duration",
            "course_price",
            "final_price",
            "categories",
            "prerequisites",
            "course_outline",
            "course_status",
            "level",
            "language",
            "discounts",
            "image",
            "instructor",
            "has_enrolled",
        ]
