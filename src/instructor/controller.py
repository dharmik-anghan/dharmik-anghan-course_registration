from rest_framework import status
from instructor.models import Instructor, Qualification
from rest_framework.response import Response
from instructor.serializers import (
    CourseInstructorSerializer,
    GetQualificationSerializer,
    InstructorSerializer,
    RegisterForInstructorSerializer,
)


def apply_for_tutor_account(request):
    try:
        # Check if the user has already applied or is already a tutor
        tutor_info = Instructor.objects.filter(instructor=request.user).first()
        if tutor_info:
            if tutor_info.application_status == "rejected":
                tutor_info.delete()
            elif tutor_info.application_status == "pending":
                raise Exception("Request already made. We will get back to you soon.")
            else:
                raise Exception(
                    "Application is already accepted. You can start posting your course"
                )
        serializer = RegisterForInstructorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(instructor=request.user)

        tutor_info = Instructor.objects.get(instructor=request.user)

        serializer = CourseInstructorSerializer(tutor_info)
        return Response(
            {
                "message": "Request for tutor account has been sent",
                "data": serializer.data,
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


def get_status_of_application(request):
    try:
        tutor_info = Instructor.objects.filter(instructor=request.user).first()

        if not tutor_info:
            raise Exception("Application not found")

        serializer = InstructorSerializer(tutor_info)

        return Response(
            {
                "message": "status of application",
                "data": {"user": serializer.data},
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


def get_qualification_details():
    try:
        quali = Qualification.objects.all()
        serializer = GetQualificationSerializer(quali, many=True)
        return Response(
            {
                "message": "qualifications",
                "data": serializer.data,
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
