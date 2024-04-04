from django.contrib import admin
from review.models import Review
from review.utils import RatingChoice


class ReviewAdmin(admin.ModelAdmin):
    model = Review

    list_display = [
        "get_account_first_name",
        "course",
        "get_enum_value",
        "created_at",
    ]

    def get_account_first_name(self, obj):
        return obj.account.first_name

    get_account_first_name.short_description = "First Name"

    def get_enum_value(self, obj):
        return obj.rating

    get_enum_value.short_description = "Rating"


admin.site.register(Review, ReviewAdmin)
