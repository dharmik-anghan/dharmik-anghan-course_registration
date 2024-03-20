from account.utils import Util
from account.models import User
from rest_framework import serializers
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


class UserRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(
        style={"input_type": "password"}, write_only=True
    )

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "password",
            "confirm_password",
            "tc",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    # Validating password and confirm password
    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")
        if password != confirm_password:
            raise serializers.ValidationError(
                "Password and Confirm Password don't match"
            )
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ["email", "password"]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password", "last_login"]


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
                "Password and Confirm Password don't match"
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
            raise Exception("You are not registred user")


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
                    "Password and Confirm Password don't match"
                )

            email = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(email=email)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise Exception("Token is not Valid or Expired")
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise Exception("Token is not Valid or Expired")


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
            raise Exception("You are not registred user")


class AuthUserEmailSerializer(serializers.Serializer):

    class Meta:
        fields = []

    def validate(self, attrs):
        try:
            uid = self.context.get("uid")
            token = self.context.get("token")
            email = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(email=email)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise Exception("Token is not Valid or Expired")
            if user.is_verified != True:
                user.is_verified = True
                user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise Exception("Token is not Valid or Expired")
