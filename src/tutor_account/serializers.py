from rest_framework import serializers

from tutor_account.models import Tutor


class TutorRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = ["qualification", "description"]


class AcceptTutorAccountRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        exclude = ["is_deleted"]


class UpdateStatusofApplicationSerializer(serializers.ModelSerializer):
    request_id = serializers.IntegerField()
    reason_for_rejection = serializers.CharField(required=False)

    class Meta:
        model = Tutor
        fields = ["request_id", "application_status", "reason_for_rejection"]

    def validate(self, attrs):

        if attrs.get("application_status") == "rejected":
            if attrs.get("reason_for_rejection") is None:
                raise Exception("'reason_for_rejection' field required")

        return attrs
