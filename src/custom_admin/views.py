from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from account.permissions import IsStaffUser
from custom_admin.controller import (
    CourseCategoryController,
    QualificationController,
    PermissionController,
    InstructorController,
)


class AdminPermissionView(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request):
        message = PermissionController.give_permission_to_user(request)
        return message


class AddQualificationView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        message = QualificationController.add_qualifications(request)
        return message

    def put(self, request):
        message = QualificationController.update_qualifications(request)
        return message

    def delete(self, request):
        message = QualificationController.delete_qualifications(request)
        return message


# Only admins/staff can accept request of users for tutor accounts
class AcceptInstructorAccountRequestView(APIView):
    permission_classes = [IsStaffUser]

    def get(self, request):
        message = InstructorController.get_registered_tutor_request(request)
        return message

    def put(self, request):
        message = InstructorController.update_tutor_application_status(request)
        return message


class AddCategoryView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        message = CourseCategoryController.add_category(request)
        return message

    def put(self, request):
        message = CourseCategoryController.update_category(request)
        return message

    def delete(self, request):
        message = CourseCategoryController.delete_category(request)
        return message
