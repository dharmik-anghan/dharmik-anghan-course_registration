from rest_framework.views import APIView
from account.permissions import IsVerified
from rest_framework.permissions import IsAdminUser
from tutor_account.controller import (
    ApplyForTutorAccount,
    GetRegisteredTutorRequest,
    GetStatusOfApplication,
    UpdateTutorApplicationStatus,
)


# Give application for tutor account. Only verified user can apply for application
class RegisterForTutorAccountView(APIView):
    permission_classes = [IsVerified]

    def post(self, request):
        message = ApplyForTutorAccount(request)
        return message


class AcceptTutorAccountRequestView(APIView):
    # Only admins can accept request of users for tutor accounts
    permission_classes = [IsAdminUser]

    def get(self, request):
        message = GetRegisteredTutorRequest(request)
        return message

    def put(self, request):
        message = UpdateTutorApplicationStatus(request)
        return message


# User can get their application status
class GetStatusOfTutorAccountApplication(APIView):
    permission_classes = [IsVerified]

    def get(self, request):
        message = GetStatusOfApplication(request)
        return message
