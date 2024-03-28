from account.permissions import IsCourseOwnerUser, IsInstructorUser
from rest_framework.views import APIView
from course.controller import (
    delete_cource,
    get_courses_details,
    register_for_course,
    update_course,
)


# Tutor and admin can register course
class UploadCourseView(APIView):
    permission_classes = [IsInstructorUser]

    def post(self, request):
        message = register_for_course(request)
        return message


# Tutor and admin can update and delete course
class CourseUpdateView(APIView):
    permission_classes = [IsCourseOwnerUser]

    def put(self, request, course_id):
        message = update_course(request, course_id)
        return message

    def delete(self, request, course_id):
        message = delete_cource(request, course_id)
        return message


# # User can get view of all course listed
class GetCourseDetailsView(APIView):
    permission_classes = [IsInstructorUser]

    def get(self, request, course_id=None):
        message = get_courses_details(request, course_id)
        return message
