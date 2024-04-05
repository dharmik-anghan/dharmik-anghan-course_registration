from rest_framework.views import APIView
from account.permissions import IsVerifiedUser
from instructor.controller import apply_for_tutor_account, get_qualification_details, get_status_of_application


# Give application for tutor account. Only verified user can apply for application
class RegisterForTutorAccountView(APIView):
    permission_classes = [IsVerifiedUser]

    def get(self, request):
        message = get_status_of_application(request)
        return message

    def post(self, request):
        message = apply_for_tutor_account(request)
        return message

class GetQualificationView(APIView):
    permission_classes = [IsVerifiedUser]

    def get(self, request):
        message = get_qualification_details()
        return message