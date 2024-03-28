from django.urls import path

from course.views import CourseUpdateView, GetCourseDetailsView, UploadCourseView

urlpatterns = [
    path("register/", UploadCourseView.as_view(), name="course-register"),
    path("update/<int:course_id>", CourseUpdateView.as_view(), name="course-update"),
    path("", GetCourseDetailsView.as_view(), name="get-courses"),
    path("<int:course_id>/", GetCourseDetailsView.as_view(), name="get-courses-by-id"),
]
