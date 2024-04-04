from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator


class UserManager(BaseUserManager):
    def create_user(
        self,
        email,
        contact_number,
        term,
        first_name=None,
        last_name=None,
        username=None,
        password=None,
        **extra_fields
    ):
        if not email and not contact_number:
            raise ValueError("Users must have an email address and contact number")

        username = username or email.split("@")[0]  # Better username generation

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            term=term,
            contact_number=contact_number,
            username=username,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        permission = UserPermission(account=user)
        permission.save()

        return user

    def create_superuser(
        self,
        email,
        contact_number,
        term,
        username=None,
        first_name=None,
        last_name=None,
        password=None,
        **extra_fields
    ):
        extra_fields.setdefault("is_admin", True)

        return self.create_user(
            email,
            contact_number,
            term,
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            **extra_fields
        )


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="Email", max_length=255, unique=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    username = models.CharField(max_length=30, null=True, blank=True, unique=True)
    contact_number = models.CharField(
        max_length=13,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^\+?1?\d{9,15}$",
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
            )
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    term = models.BooleanField()

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["term", "contact_number"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class UserPermission(models.Model):
    account = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="permission"
    )
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_instructor = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
