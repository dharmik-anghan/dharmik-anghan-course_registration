from django.urls import path
from instructor.views import GetQualificationView, RegisterForTutorAccountView


urlpatterns = [
    path(
        "register/",
        RegisterForTutorAccountView.as_view(),
        name="register-tutor-account",
    ),
    path(
        "qualification/",
        GetQualificationView.as_view(),
        name="get-qualification",
    ),
]
