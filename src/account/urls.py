from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from account.views import (
    AuthUserEmailView,
    SentAuthLinkEmailView,
    SentResetPasswordEmailView,
    UserChangePasswordView,
    UserLoginView,
    UserPasswordResetView,
    UserProfileView,
    UserRegistrationView,
)

urlpatterns = [
    path("token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("change-password/", UserChangePasswordView.as_view(), name="change-password"),
    path(
        "sent-reset-password-email/",
        SentResetPasswordEmailView.as_view(),
        name="sent-reset-password-email",
    ),
    path(
        "reset-password/<uid>/<token>/",
        UserPasswordResetView.as_view(),
        name="reset-password",
    ),
    path(
        "sent-auth-email/",
        SentAuthLinkEmailView.as_view(),
        name="sent-auth-email",
    ),
    path(
        "verifyaccount/<uid>/<token>/",
        AuthUserEmailView.as_view(),
        name="verifyaccount",
    ),
]
