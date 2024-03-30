from rest_framework.views import APIView
from account.permissions import HasPurchasedCourse, IsVerifiedUser
from review.controller import post_review, update_review, get_review, delete_review


class ReviewView(APIView):
    permission_classes = [HasPurchasedCourse]

    def post(self, request, course_id):
        message = post_review(request, course_id)
        return message

    def put(self, request, course_id):
        message = update_review(request, course_id)
        return message

    def delete(self, request, course_id):
        message = delete_review(request, course_id)
        return message


class GetReviewView(APIView):
    permission_classes = [IsVerifiedUser]

    def get(self, request, course_id):
        message = get_review(request, course_id)
        return message
