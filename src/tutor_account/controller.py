from datetime import datetime, timezone
from rest_framework import status
from tutor_account.models import Tutor
from rest_framework.response import Response
from tutor_account.serializers import (
    AcceptTutorAccountRequestSerializer,
    TutorRegistrationSerializer,
    UpdateStatusofApplicationSerializer,
)


def ApplyForTutorAccount(request):
    try:
        if Tutor.objects.filter(account=request.user).exists():
            tutor_info = Tutor.objects.get(account=request.user)

            if tutor_info.application_status == "rejected":
                tutor_info.delete()
            elif tutor_info.application_status == "pending":
                raise Exception(
                    "Request already been made. We will get back to you soon."
                )
            else:
                raise Exception(
                    "Application is already accepted. You can start posting your course"
                )
        serializer = TutorRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(account=request.user)
        return Response(
            {
                "message": "Request for tutor account has been sent",
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


def GetRegisteredTutorRequest(request):
    try:
        request_id = request.data.get("request_id")
        if request_id:
            tutor_request = Tutor.objects.filter(pk=request_id).all()
        else:
            tutor_request = Tutor.objects.filter().all()

        if not tutor_request:
            raise Exception("No Request Found")
        serializer = AcceptTutorAccountRequestSerializer(tutor_request, many=True)

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


def UpdateTutorApplicationStatus(request):
    try:
        serializer = UpdateStatusofApplicationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tutor_info = Tutor.objects.get(pk=serializer.data.get("request_id"))

        if tutor_info.application_accepted:
            raise Exception(
                "Application is already accepted. You can start posting your course"
            )
        if tutor_info.application_status != "pending":
            raise Exception("Application status has updated")

        tutor_info.application_accepted_by = request.user
        tutor_info.accepted_at = datetime.now(timezone.utc)
        tutor_info.application_status = serializer.data.get("application_status")

        if serializer.data.get("application_status") == "accepted":
            tutor_info.application_accepted = True
            tutor_info.account.is_tutor = True
            tutor_info.account.save()  # Update account table
        elif serializer.data.get("application_status") == "rejected":
            tutor_info.reason_for_rejection = serializer.data.get(
                "reason_for_rejection"
            )

        tutor_info.save()  # Update tutor_account table

        serializer = AcceptTutorAccountRequestSerializer(tutor_info)

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


def GetStatusOfApplication(request):
    try:
        tutor_info = Tutor.objects.filter(account=request.user).first()

        if not tutor_info:
            raise Exception("Application not found")

        serializer = AcceptTutorAccountRequestSerializer(tutor_info)

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
