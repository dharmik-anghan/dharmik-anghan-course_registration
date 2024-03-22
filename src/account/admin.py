from django.contrib import admin
from account.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserModelAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserModelAdmin
    # that reference specific fields on auth.User.
    list_display = [
        "id",
        "email",
        "first_name",
        "last_name",
        "term",
        "is_admin",
        "is_tutor",
    ]
    list_filter = ["is_admin"]
    fieldsets = [
        ("User Credentials", {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["first_name", "last_name", "term"]}),
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
                    "last_name",
                    "term",
                    "password1",
                    "confirm_password",
                ],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email", "id"]
    filter_horizontal = []
    list_editable = ["is_admin", "is_tutor"]


admin.site.register(User, UserModelAdmin)
