from account.permissions import IsCourseOwner, IsTutor, IsVerified
from rest_framework.views import APIView
from course.controller import (
    delete_tutor_cource,
    get_courses_details,
    register_tutor_course,
    update_tutor_course,
)


# Tutor and admin can register course
class CourseTutorRegistrationView(APIView):
    permission_classes = [IsTutor]

    def post(self, request):
        message = register_tutor_course(request)
        return message


# Tutor and admin can update and delete course
class CourseUpdateView(APIView):
    permission_classes = [IsCourseOwner]

    def put(self, request, course_id):
        message = update_tutor_course(request, course_id)
        return message

    def delete(self, request, course_id):
        message = delete_tutor_cource(request, course_id)
        return message


# User can get view of all course listed
class GetCourseDetailsView(APIView):
    permission_classes = [IsVerified]

    def get(self, request, course_id=None):
        message = get_courses_details(request, course_id)
        return message
