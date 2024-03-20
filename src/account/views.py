from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from account.controller import (
    authUserEmail,
    getUserProfile,
    sentAuthLinkEmail,
    sentResetPasswordEmail,
    userChangePassword,
    userLogin,
    userPasswordResetView,
    userRegistration,
)
from account.permissions import IsVerified


# Register User.
class UserRegistrationView(APIView):

    def post(self, request):
        message = userRegistration(request)
        return message


# Login User
class UserLoginView(APIView):

    def post(self, request):
        message = userLogin(request)
        return message


# Get user profile
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        message = getUserProfile(request)
        return message


# Change user password
class UserChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        message = userChangePassword(request)
        return message


# Sent password reset link to email
class SentResetPasswordEmailView(APIView):

    def post(self, request):
        message = sentResetPasswordEmail(request)
        return message


# Reset password
class UserPasswordResetView(APIView):

    def put(self, request, uid, token):
        message = userPasswordResetView(request, uid, token)
        return message


# Sent link to user for verification
class SentAuthLinkEmailView(APIView):

    def post(self, request):
        message = sentAuthLinkEmail(request)
        return message


# Verify Email
class AuthUserEmailView(APIView):

    def post(self, request, uid, token):
        message = authUserEmail(request)
        return message
