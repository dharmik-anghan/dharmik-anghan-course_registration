from rest_framework import permissions

from course.models import Course


class IsTutor(permissions.BasePermission):
    message = (
        "Access Denied. You don't have tutor account. You can apply at our portal."
    )

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        user = request.user.is_tutor
        return bool(user and request.user.is_authenticated)


class IsVerified(permissions.BasePermission):
    message = "Verify Your Email To Access"

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        is_verified = request.user.is_verified
        return bool(is_verified and request.user.is_authenticated)


class IsCourseOwner(permissions.BasePermission):
    message = "Don't have permission to change course details. Only course owner can change details"

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False

        if request.user.is_admin:
            return True

        course_id = request.parser_context.get("kwargs").get("course_id")
        course_info = Course.objects.filter(pk=course_id).first()

        if course_info is not None:
            if course_info.tutor_id != request.user.id:
                return False
        user = request.user.is_tutor
        return bool(user and request.user.is_authenticated)
