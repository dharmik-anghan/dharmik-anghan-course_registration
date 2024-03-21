from rest_framework.views import APIView
from account.permissions import IsVerified
from rest_framework.permissions import IsAdminUser
from tutor_account.controller import (
    apply_for_tutor_account,
    get_registered_tutor_request,
    get_status_of_application,
    update_tutor_application_status,
)


# Give application for tutor account. Only verified user can apply for application
class RegisterForTutorAccountView(APIView):
    permission_classes = [IsVerified]

    def post(self, request):
        message = apply_for_tutor_account(request)
        return message


# Only admins can accept request of users for tutor accounts
class AcceptTutorAccountRequestView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        message = get_registered_tutor_request(request)
        return message

    def put(self, request):
        message = update_tutor_application_status(request)
        return message


# User can get their application status
class GetStatusOfTutorAccountApplication(APIView):
    permission_classes = [IsVerified]

    def get(self, request):
        message = get_status_of_application(request)
        return message
