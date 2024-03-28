from django.urls import path
from custom_admin.views import (
    AcceptInstructorAccountRequestView,
    AddCategoryView,
    AddQualificationView,
    AdminPermissionView,
)

urlpatterns = [
    path("user/role/", AdminPermissionView.as_view(), name="role"),
    path(
        "instructor/qualification/",
        AddQualificationView.as_view(),
        name="qualification",
    ),
    path(
        "instructor/profile/",
        AcceptInstructorAccountRequestView.as_view(),
        name="tutor-profile",
    ),
    path(
        "course/category/",
        AddCategoryView.as_view(),
        name="course-category",
    ),
]
