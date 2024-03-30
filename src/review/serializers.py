from rest_framework import serializers
from review.models import Review


class PostReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = [
            "review",
            "rating",
            "created_at",
        ]


class GetReviewSerializer(serializers.ModelSerializer):

    name = serializers.CharField(source="account.first_name", read_only=True)

    class Meta:
        model = Review
        fields = [
            "account",
            "name",
            "course",
            "review",
            "rating",
            "created_at",
            "updated_at",
        ]
