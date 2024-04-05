from datetime import datetime, timezone
from rest_framework import status
from course.models import Category
from instructor.models import Qualification, Instructor
from rest_framework.response import Response
from account.models import User, UserPermission
from django.core.exceptions import ObjectDoesNotExist
from account.serializers import UserPermissionSerializer
from custom_admin.serializers import (
    CourseCategoryserializer,
    InstructorSerializer,
    AddQualificationSerializer,
    UpdateStatusofApplicationSerializer,
)
from instructor.utils import ApplicationStatusEnum


class PermissionController:
    @staticmethod
    def give_permission_to_user(request):
        try:
            account = request.data.get("account_id")
            user = UserPermission.objects.get(account=account)
            serializer = UserPermissionSerializer(user, request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {
                    "message": "user permission updated",
                    "data": serializer.data,
                    "status": "success",
                    "status_code": 200,
                },
                status=status.HTTP_200_OK,
            )
        except UserPermission.DoesNotExist:
            return Response(
                {
                    "message": "user not found",
                    "status": "error",
                    "status_code": 404,
                },
                status=404,
            )
        except Exception as e:
            return Response(
                {"message": f"{str(e)}", "status": "error", "status_code": 400},
                status=400,
            )


class QualificationController:
    @staticmethod
    def add_qualifications(request):
        serializer = AddQualificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "message": "qualification added successfully",
                "status": "success",
                "status_code": 201,
            },
            status=201,
        )

    @staticmethod
    def update_qualifications(request):
        try:
            id = request.query_params.get("id")
            qualification = Qualification.objects.get(pk=id)
            serializer = AddQualificationSerializer(
                qualification, request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {
                    "message": "qualification updated successfully",
                    "status": "success",
                    "status_code": 200,
                },
                status=200,
            )
        except Qualification.DoesNotExist or ObjectDoesNotExist:
            return Response(
                {
                    "message": "qualification not found",
                    "status": "error",
                    "status_code": 404,
                },
                status=404,
            )
        except Exception as e:
            return Response(
                {"message": f"{str(e)}", "status": "error", "status_code": 400},
                status=400,
            )

    @staticmethod
    def delete_qualifications(request):
        try:
            id = request.query_params.get("id")
            qualification = Qualification.objects.get(pk=id)
            qualification.delete()
            return Response(
                {
                    "message": "qualification deleted successfully",
                    "status": "success",
                    "status_code": 204,
                },
                status=204,
            )
        except Qualification.DoesNotExist or ObjectDoesNotExist:
            return Response(
                {
                    "message": "qualification not found",
                    "status": "error",
                    "status_code": 404,
                },
                status=404,
            )
        except Exception as e:
            return Response(
                {"message": f"{str(e)}", "status": "error", "status_code": 400},
                status=400,
            )


class InstructorController:
    @staticmethod
    def get_registered_tutor_request(request):
        try:
            request_id = request.query_params.get("id")
            if request_id:
                tutor_request = Instructor.objects.filter(pk=request_id).all()
            else:
                tutor_request = Instructor.objects.filter().all()

            if not tutor_request:
                raise Exception("no instructor account request found")
            serializer = InstructorSerializer(tutor_request, many=True)

            return Response(
                {
                    "message": {"user": serializer.data},
                    "status": "success",
                    "status_code": 200,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"message": f"{str(e)}", "status": "error", "status_code": 400},
                status=400,
            )

    @staticmethod
    def update_tutor_application_status(request):
        try:
            serializer = UpdateStatusofApplicationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            application_status = serializer.validated_data.get("application_status")
            instructor_id = serializer.validated_data.get("instructor_id")
            reason_for_rejection = serializer.validated_data.get("reason_for_rejection")

            instructor = Instructor.objects.get(instructor=instructor_id)
            if instructor.instructor.is_admin == True and request.user.is_admin != True:
                raise Exception(
                    "you don't have admin role. only admin can accept/reject admin application"
                )

            # if application is accepted raise exception if already accepted
            if (
                instructor.application_status == application_status
                and instructor.application_status == ApplicationStatusEnum.ACCEPTED
            ):
                raise Exception("application is already accepted")

            instructor.accepted_by = request.user
            instructor.accepted_at = datetime.now(timezone.utc)
            instructor.application_status = application_status

            # if application accepted or rejected update permissionś
            user_permission = UserPermission.objects.get(
                account=instructor.instructor.id
            )
            if application_status == ApplicationStatusEnum.ACCEPTED:
                user_permission.is_instructor = True
            elif (
                application_status == ApplicationStatusEnum.REJECTED
                or application_status == ApplicationStatusEnum.PENDING
            ):
                instructor.reason_for_rejection = reason_for_rejection
                user_permission.is_instructor = False

            user_permission.save()
            instructor.save()  # Update tutor_account table

            serializer = InstructorSerializer(instructor)

            return Response(
                {
                    "message": "application updated",
                    "data": {"user": serializer.data},
                    "status": "success",
                    "status_code": 200,
                },
                status=status.HTTP_200_OK,
            )
        except Instructor.DoesNotExist or ObjectDoesNotExist:
            return Response(
                {"message": "user not found", "status": "error", "status_code": 404},
                status=404,
            )
        except Exception as e:
            return Response(
                {"message": f"{str(e)}", "status": "error", "status_code": 400},
                status=400,
            )


class CourseCategoryController:

    @staticmethod
    def add_category(request):
        try:
            serializer = CourseCategoryserializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {
                    "message": "Category '{}' added".format(
                        serializer.validated_data.get("name")
                    ),
                    "status": "success",
                    "status_code": 201,
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"message": f"{str(e)}", "status": "error", "status_code": 400},
                status=400,
            )

    @staticmethod
    def update_category(request):
        try:
            category_id = request.query_params.get("category_id")
            category = Category.objects.get(pk=category_id)
            serializer = CourseCategoryserializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            name = serializer.validated_data.get("name")

            category.name = name
            category.save()

            return Response(
                {
                    "message": "Category '{}' updated".format(
                        serializer.validated_data.get("name")
                    ),
                    "status": "success",
                    "status_code": 200,
                },
                status=status.HTTP_200_OK,
            )
        except Category.DoesNotExist or ObjectDoesNotExist:
            return Response(
                {
                    "message": "category not found",
                    "status": "error",
                    "status_code": 404,
                },
                status=404,
            )
        except Exception as e:
            return Response(
                {"message": f"{str(e)}", "status": "error", "status_code": 400},
                status=400,
            )

    @staticmethod
    def delete_category(request):
        try:
            category_id = request.query_params.get("category_id")
            category = Category.objects.get(pk=category_id)

            category.delete()

            return Response(
                {
                    "message": "Category deleted",
                    "status": "success",
                    "status_code": 204,
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        except Category.DoesNotExist or ObjectDoesNotExist:
            return Response(
                {
                    "message": "category not found",
                    "status": "error",
                    "status_code": 404,
                },
                status=404,
            )
        except Exception as e:
            return Response(
                {"message": f"{str(e)}", "status": "error", "status_code": 400},
                status=400,
            )
