from account.utils import Util
from rest_framework import serializers
from account.models import User, UserPermission
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


class UserPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPermission
        fields = ["account", "is_staff", "is_verified", "is_instructor"]


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "password",
            "contact_number",
            "term",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        term = attrs.get("term")
        if not term:
            raise serializers.ValidationError("Accept terms and conditions to proceed")
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ["email", "password"]


class UserProfileSerializer(serializers.ModelSerializer):
    def get_user_permissions(self, obj):
        request = self.context.get("request")
        user = request.user
        permissions = UserPermission.objects.filter(account=user).first()
        serializer = UserPermissionSerializer(permissions)
        return serializer.data

    permissions = serializers.SerializerMethodField("get_user_permissions")

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "contact_number",
            "created_at",
            "is_active",
            "is_admin",
            "is_deleted",
            "term",
            "permissions",
        ]


class UserChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        max_length=255, write_only=True, style={"input_type": "password"}
    )
    confirm_password = serializers.CharField(
        max_length=255, write_only=True, style={"input_type": "password"}
    )

    class Meta:
        fields = ["new_password", "confirm_password"]

    def validate(self, attrs):
        password = attrs.get("new_password")
        confirm_password = attrs.get("confirm_password")
        user = self.context.get("user")
        if password != confirm_password:
            raise serializers.ValidationError(
                "password and confirm password don't match"
            )
        user.set_password(password)
        user.save()
        return attrs


class SentResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ["email"]

    def validate(self, attrs):
        email = attrs.get("email")
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.email))
            token = PasswordResetTokenGenerator().make_token(user)
            link = "http://localhost:3000/api/user/reset/" + uid + "/" + token
            body = "Click Following Link To Reset Your Password " + link
            data = {"subject": "Reset Password", "body": body, "to_email": user.email}
            Util.sent_email(data)
            return attrs

        else:
            raise Exception("user is not registered")


class UserPasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        max_length=255, write_only=True, style={"input_type": "password"}
    )
    confirm_password = serializers.CharField(
        max_length=255, write_only=True, style={"input_type": "password"}
    )

    class Meta:
        fields = ["new_password", "confirm_password"]

    def validate(self, attrs):
        try:
            password = attrs.get("new_password")
            confirm_password = attrs.get("confirm_password")
            uid = self.context.get("uid")
            token = self.context.get("token")
            if password != confirm_password:
                raise serializers.ValidationError(
                    "password and confirm password don't match"
                )

            email = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(email=email)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise Exception("token is not valid or expired")
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise Exception("token is not valid or expired")


class SentAuthLinkEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ["email"]

    def validate(self, attrs):
        email = attrs.get("email")
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.email))
            token = PasswordResetTokenGenerator().make_token(user)
            link = "http://localhost:3000/api/user/verify/" + uid + "/" + token
            body = "Click Following Link To Verify Your Account " + link
            data = {"subject": "Verify Account", "body": body, "to_email": user.email}
            Util.sent_email(data)
            return attrs

        else:
            raise Exception("user is not registered")


class AuthUserEmailSerializer(serializers.Serializer):

    class Meta:
        fields = []

    def validate(self, attrs):
        uid = self.context.get("uid")
        token = self.context.get("token")
        try:
            email = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(email=email)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError("Token is not valid or expired")

            auth_user = UserPermission.objects.get(account=user)

            if not auth_user.is_verified:
                auth_user.is_verified = True
                auth_user.save()

        except (ObjectDoesNotExist, DjangoUnicodeDecodeError):  # Combine exceptions
            raise serializers.ValidationError("User or token is not valid or expired")

        return attrs
