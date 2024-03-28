from django.contrib import admin
from account.models import User, UserPermission
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserModelAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserModelAdmin
    # that reference specific fields on auth.User.
    list_display = [
        "id",
        "email",
        "username",
        "first_name",
        "last_name",
        "term",
        "is_admin",
        "is_deleted",
    ]
    list_filter = ["is_admin", "username"]
    fieldsets = [
        ("User Credentials", {"fields": ["email", "password"]}),
        ("Personal inf", {"fields": ["first_name", "last_name", "term"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]

    # add_fieldsets will be used when we create user thrue admin panel
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": [
                    "email",
                    "first_name",
                    "username",
                    "last_name",
                    "term",
                    "password1",
                ],
            },
        ),
    ]
    search_fields = ["email", "username"]
    ordering = ["email", "id"]
    filter_horizontal = []
    list_editable = ["is_admin", "is_deleted"]


admin.site.register(User, UserModelAdmin)


class UserPermissionAdmin(admin.ModelAdmin):
    list_display = [
        "account",
        "is_staff",
        "is_verified",
        "is_instructor",
        "created_at",
    ]
    list_editable = ["is_staff", "is_verified", "is_instructor"]

    list_filter = [
        "is_staff",
        "is_verified",
        "is_instructor",
        "created_at",
    ]

    search_fields = ["account__email"]


admin.site.register(UserPermission, UserPermissionAdmin)
