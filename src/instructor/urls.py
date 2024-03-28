from django.urls import path

from instructor.views import RegisterForTutorAccountView


urlpatterns = [
    path(
        "register/",
        RegisterForTutorAccountView.as_view(),
        name="register-tutor-account",
    )
]
