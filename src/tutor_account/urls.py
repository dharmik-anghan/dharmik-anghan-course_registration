from django.urls import path

from tutor_account.views import AcceptTutorAccountRequestView, GetStatusOfTutorAccountApplication, RegisterForTutorAccountView

urlpatterns = [
    path("register/", RegisterForTutorAccountView.as_view(), name="tutor-register"),
    path("profile/", AcceptTutorAccountRequestView.as_view(), name="tutor-profile"),
    path("status/", GetStatusOfTutorAccountApplication.as_view(), name="status"),
]