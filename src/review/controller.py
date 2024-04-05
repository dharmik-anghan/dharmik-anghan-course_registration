from course.models import Course
from review.models import Review
from django.db.models import Avg
from rest_framework import status
from django.db import transaction
from rest_framework.response import Response
from review.serializers import GetReviewSerializer, PostReviewSerializer


@transaction.atomic
def count_average_rating(course_id):
    stat = (
        Review.objects.filter(course=course_id)
        .all()
        .aggregate(Avg("rating"))["rating__avg"]
    )
    course = Course.objects.get(pk=course_id)
    course.rating = stat
    course.save()


def post_review(request, course_id):
    try:
        data = request.data
        data["account"] = request.user.id
        data["course"] = course_id

        review_exists = Review.objects.filter(
            account=data["account"], course=data["course"]
        ).exists()
        course = Course.objects.get(pk=course_id)
        if review_exists:
            raise Exception("review exists")
        serializer = PostReviewSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            serializer.save(account=request.user, course=course)
            count_average_rating(course_id)

        return Response(
            {
                "message": "review posted",
                "data": {"review": serializer.data},
                "status": "success",
                "status_code": 200,
            },
            status=status.HTTP_200_OK,
        )
    except Course.DoesNotExist:
        return Response(
            {"message": "cousre not found", "status": "error", "status_code": 404},
            status=404,
        )

    except Exception as e:
        return Response(
            {"message": f"{str(e)}", "status": "error", "status_code": 400},
            status=400,
        )


def update_review(request, course_id):
    try:
        data = request.data
        data["account"] = request.user.id
        data["course"] = course_id
        data["review_id"] = request.query_params.get("review_id")

        review = Review.objects.get(
            pk=data["review_id"], account=data["account"], course=data["course"]
        )

        serializer = PostReviewSerializer(review, data, partial=True)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            serializer.save()
            count_average_rating(course_id)

        return Response(
            {
                "message": "review updated",
                "data": {"review": serializer.data},
                "status": "success",
                "status_code": 200,
            },
            status=status.HTTP_200_OK,
        )

    except Review.DoesNotExist:
        return Response(
            {"message": "review not found", "status": "error", "status_code": 404},
            status=404,
        )
    except Exception as e:
        return Response(
            {"message": f"{str(e)}", "status": "error", "status_code": 400},
            status=400,
        )


def delete_review(request, course_id):
    try:
        data = request.data
        data["account"] = request.user.id
        data["course"] = course_id
        data["review_id"] = request.query_params.get("review_id")

        review = Review.objects.get(
            pk=data["review_id"], account=data["account"], course=data["course"]
        )
        if review.account != request.user and not request.user.is_admin:
            raise Exception("cant perform this action")

        review.delete()

        with transaction.atomic():
            count_average_rating(course_id)

        return Response(
            {
                "message": "review deleted",
                "status": "success",
                "status_code": 204,
            },
            status=status.HTTP_204_NO_CONTENT,
        )

    except Review.DoesNotExist:
        return Response(
            {"message": "review not found", "status": "error", "status_code": 404},
            status=404,
        )
    except Exception as e:
        return Response(
            {"message": f"{str(e)}", "status": "error", "status_code": 400},
            status=400,
        )


def get_review(request, course_id):
    try:
        data = request.data
        data["course"] = course_id

        Course.objects.get(pk=course_id)

        review = Review.objects.filter(course=data["course"]).all()

        serializer = GetReviewSerializer(review, many=True)

        return Response(
            {
                "message": "reviews success",
                "data": {"review": serializer.data},
                "status": "success",
                "status_code": 200,
            },
            status=status.HTTP_200_OK,
        )
    except Course.DoesNotExist:
        return Response(
            {"message": "cousre not found", "status": "error", "status_code": 404},
            status=404,
        )
    except Exception as e:
        return Response(
            {"message": f"{str(e)}", "status": "error", "status_code": 400},
            status=400,
        )
