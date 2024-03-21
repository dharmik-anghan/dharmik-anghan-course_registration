from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from account.controller import (
    auth_user_email,
    get_user_profile,
    sent_auth_link_email,
    sent_reset_password_email,
    user_change_password,
    user_login,
    user_password_reset,
    user_registration,
)


# Register User.
class UserRegistrationView(APIView):

    def post(self, request):
        message = user_registration(request)
        return message


# Login User
class UserLoginView(APIView):

    def post(self, request):
        message = user_login(request)
        return message


# Get user profile
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        message = get_user_profile(request)
        return message


# Change user password
class UserChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        message = user_change_password(request)
        return message


# Sent password reset link to email
class SentResetPasswordEmailView(APIView):

    def post(self, request):
        message = sent_reset_password_email(request)
        return message


# Reset password
class UserPasswordResetView(APIView):

    def put(self, request, uid, token):
        message = user_password_reset(request, uid, token)
        return message


# Sent link to user for verification
class SentAuthLinkEmailView(APIView):

    def post(self, request):
        message = sent_auth_link_email(request)
        return message


# Verify Email
class AuthUserEmailView(APIView):

    def post(self, request, uid, token):
        message = auth_user_email(request)
        return message
