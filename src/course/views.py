from account.permissions import IsCourseOwner, IsTutor, IsVerified
from rest_framework.views import APIView
from course.controller import (
    deleteTutorCource,
    getCoursesDetails,
    registerTutorCourse,
    updateTutorCourse,
)


class CourseTutorRegistrationView(APIView):
    permission_classes = [IsTutor]

    def post(self, request):
        message = registerTutorCourse(request)
        return message


class CourseUpdateView(APIView):
    permission_classes = [IsCourseOwner]

    def put(self, request, course_id):
        message = updateTutorCourse(request, course_id)
        return message

    def delete(self, request, course_id):
        message = deleteTutorCource(request, course_id)
        return message


class GetCourseDetailsView(APIView):
    permission_classes = [IsVerified]

    def get(self, request, course_id=None):
        message = getCoursesDetails(request, course_id)
        return message
