from rest_framework.views import APIView
from account.permissions import IsVerifiedUser
from student.controller import (
    course_purchase,
    course_unregistration,
    get_my_course,
    search_courses,
)


# Register for course
class CourseRegistrationView(APIView):
    permission_classes = [IsVerifiedUser]

    def post(self, request, course_id: int):
        message = course_purchase(request, course_id)
        return message


# UnRegister for course
class CourseUnRegistrationView(APIView):
    permission_classes = [IsVerifiedUser]

    def delete(self, request, course_id: int):
        message = course_unregistration(request, course_id)
        return message


# Current users courses which he has enrolled in
class EnrolledCourseView(APIView):
    permission_classes = [IsVerifiedUser]

    def get(self, request, course_id: int = None):
        message = get_my_course(request, course_id)
        return message


# Verified user can search course by course title
class SearchCourseView(APIView):
    permission_classes = [IsVerifiedUser]

    def get(self, request):
        message = search_courses(request)
        return message
