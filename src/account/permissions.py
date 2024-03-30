from course.models import Course
from rest_framework import permissions
from account.models import UserPermission
from student.models import CoursePurchase


class IsStaffUser(permissions.BasePermission):
    message = "Access Denied."

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False

        try:
            user_permission = UserPermission.objects.get(account=request.user)

            # Allow staff users to perform all actions except DELETE
            if request.user.is_admin or (
                user_permission.is_staff and request.method != "DELETE"
            ):
                return True

        except UserPermission.DoesNotExist:
            return False

        return False


class IsInstructorUser(permissions.BasePermission):
    message = (
        "access denied. you don't have tutor account. you can apply at our portal."
    )

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False

        try:
            user_permission = UserPermission.objects.get(account=request.user)

            if not user_permission.is_verified:
                return False

            # Allow staff users to perform all actions except DELETE
            if (
                request.user.is_admin
                or user_permission.is_instructor
                or (user_permission.is_staff and request.method != "DELETE")
            ):
                return True

        except UserPermission.DoesNotExist:
            return False

        return False


class IsVerifiedUser(permissions.BasePermission):
    message = "verify your email to access"

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False

        try:
            user_permission = UserPermission.objects.get(account=request.user)

            # admin and verified user can access such apis
            if request.user.is_admin or user_permission.is_verified:
                return True

        except UserPermission.DoesNotExist:
            return False

        return False


class IsCourseOwnerUser(permissions.BasePermission):
    message = "only course owner has access"

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        # admin and verified user can access such apis
        if request.user.is_admin:
            return True
        try:
            user_permission = UserPermission.objects.get(account=request.user)

            course_id = request.parser_context.get("kwargs").get("course_id")
            course_info = Course.objects.filter(pk=course_id).first()

            if course_info is not None:
                if (
                    course_info.instructor.id == request.user.id
                    and user_permission.is_instructor
                ):
                    return True
            else:
                return False
        except UserPermission.DoesNotExist or Course.DoesNotExist:
            return False


class HasPurchasedCourse(permissions.BasePermission):
    message = "you can review only purchased course"

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False

        if request.user.is_admin:
            return True
        course_id = request.parser_context.get("kwargs").get("course_id")
        purchase_info = CoursePurchase.objects.filter(
            student=request.user, course=course_id, is_registered=True
        ).exists()

        if purchase_info:
            return True

        return False
