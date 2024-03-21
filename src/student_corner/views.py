from rest_framework.views import APIView
from account.permissions import IsVerified
from student_corner.controller import (
    course_registration,
    course_unregistration,
    get_my_course,
    search_courses,
)


# Register for course
class CourseRegistrationView(APIView):
    permission_classes = [IsVerified]

    def post(self, request, course_id: int):
        message = course_registration(request, course_id)
        return message


# UnRegister for course
class CourseUnRegistrationView(APIView):
    permission_classes = [IsVerified]

    def delete(self, request, course_id: int):
        message = course_unregistration(request, course_id)
        return message


# Current users courses which he has enrolled in
class EnrolledCourseView(APIView):
    permission_classes = [IsVerified]

    def get(self, request, course_id: int = None):
        message = get_my_course(request, course_id)
        return message


# Verified user can search course by course title
class SearchCourseView(APIView):
    permission_classes = [IsVerified]

    def get(self, request):
        message = search_courses(request)
        return message