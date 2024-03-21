from datetime import datetime, timezone
from account.utils import Util
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate

from account.serializers import (
    AuthUserEmailSerializer,
    SentAuthLinkEmailSerializer,
    SentResetPasswordEmailSerializer,
    UserChangePasswordSerializer,
    UserLoginSerializer,
    UserPasswordResetSerializer,
    UserProfileSerializer,
    UserRegisterSerializer,
)


def user_registration(request):
    try:
        serializer = UserRegisterSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Util.get_tokens_for_user(user)
        return Response(
            {
                "message": "User Registration Success",
                "data": {"token": token},
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


def user_login(request):
    try:
        serializer = UserLoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        email = serializer.data.get("email")
        password = serializer.data.get("password")
        user = authenticate(email=email, password=password)

        if user is not None:
            user.last_login = datetime.now(timezone.utc)
            user.save()
            token = Util.get_tokens_for_user(user)

            return Response(
                {
                    "message": "User Login Success",
                    "data": {"token": token},
                    "status": "success",
                    "status_code": 200,
                },
                status=status.HTTP_200_OK,
            )
        else:
            raise Exception("Email or password is not valid")
    except Exception as e:
        return Response(
            {"message": f"{str(e)}", "status": "error", "status_code": 400},
            status=400,
        )


def get_user_profile(request):
    try:
        serializer = UserProfileSerializer(request.user)
        return Response(
            {
                "message": "User Found Success",
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


def user_change_password(request):
    try:
        user = authenticate(
            email=request.user.email, password=request.data["old_password"]
        )
        if user:
            serializer = UserChangePasswordSerializer(
                data=request.data, context={"user": request.user}
            )
            serializer.is_valid(raise_exception=True)
            return Response(
                {
                    "message": "Password Changed Success",
                    "status": "success",
                    "status_code": 200,
                },
                status=status.HTTP_200_OK,
            )
        else:
            raise Exception("Old password does not match")
    except Exception as e:
        return Response(
            {"message": f"{str(e)}", "status": "error", "status_code": 400},
            status=400,
        )


def sent_reset_password_email(request):
    try:
        serializer = SentResetPasswordEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {
                "message": "Password Reset link send. Please check your Email.",
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


def user_password_reset(request, uid, token):
    try:
        serializer = UserPasswordResetSerializer(
            data=request.data, context={"uid": uid, "token": token}
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            {
                "message": "Password Reset Successfully.",
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


def sent_auth_link_email(request):
    try:
        serializer = SentAuthLinkEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {
                "message": "Link Sent Successfully",
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


def auth_user_email(request, uid, token):
    try:
        serializer = AuthUserEmailSerializer(
            data=request.data, context={"uid": uid, "token": token}
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            {
                "message": "Account Verified Successfully",
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
