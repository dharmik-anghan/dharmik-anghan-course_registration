from django.urls import path

from course.views import CourseTutorRegistrationView, CourseUpdateView, GetCourseDetailsView

urlpatterns = [
    path("register/", CourseTutorRegistrationView.as_view(), name="course-register"),
    path("update/<int:course_id>", CourseUpdateView.as_view(), name="course-update"),
    path("courses/", GetCourseDetailsView.as_view(), name="get-courses"),
    path("courses/<int:course_id>/", GetCourseDetailsView.as_view(), name="get-courses-by-id"),
]
