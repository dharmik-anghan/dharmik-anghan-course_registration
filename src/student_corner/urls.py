from django.urls import path

from student_corner.views import (
    CourseRegistrationView,
    CourseUnRegistrationView,
    EnrolledCourseView,
    SearchCourseView,
)

urlpatterns = [
    path(
        "register/<int:course_id>",
        CourseRegistrationView.as_view(),
        name="register-for-course",
    ),
    path(
        "unregister/<int:course_id>",
        CourseUnRegistrationView.as_view(),
        name="unregister-for-course",
    ),
    path(
        "mycourses/",
        EnrolledCourseView.as_view(),
        name="mycourses",
    ),
    path(
        "mycourses/<int:course_id>",
        EnrolledCourseView.as_view(),
        name="mycourses-for-course",
    ),
    path(
        "search/",
        SearchCourseView.as_view(),
        name="search-course",
    ),
]
