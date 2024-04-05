from course.models import Course
from rest_framework import status
from django.db import transaction
from rest_framework.response import Response
from course.serializers import InstructorandCourseDetailsSerializer
from student.models import CoursePurchase
from student.serializers import RegisterForCourseSerializer
from django.core.exceptions import ObjectDoesNotExist


@transaction.atomic
def update_student_count_and_cash_earned(course_id, fees):
    student_count = CoursePurchase.objects.filter(
        course=course_id, is_registered=True
    ).count()
    course = Course.objects.get(id=course_id, is_deleted=False)
    course.student_count = student_count
    course.instructor.money_earned += fees
    course.instructor.save()
    course.save()


def course_purchase(request, course_id):
    try:
        course = Course.objects.get(id=course_id, is_deleted=False)
        is_registered_student = CoursePurchase.objects.filter(
            course=course_id, student=request.user, is_registered=True
        ).exists()

        if is_registered_student:
            raise Exception("you have already enrolled in course")

        if course.instructor.instructor == request.user:
            raise Exception(
                "course owner have access to their course. can't purchase their own course."
            )

        if (
            CoursePurchase.objects.filter(
                course=course_id, student=request.user
            ).exists()
            and not is_registered_student
        ):
            reg_course = CoursePurchase.objects.get(
                course=course_id,
                student=request.user,
                is_registered=False,
            )
            reg_course.is_registered = True
            reg_course.save()
        else:
            data = {}

            data["course"] = course_id
            data["student"] = request.user.id

            course_price = course.course_price - (
                course.course_price * course.discounts * 0.01
            )

            serializer = RegisterForCourseSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                serializer.save(fees_paid=course_price)
                update_student_count_and_cash_earned(course_id, course_price)
        serializer = InstructorandCourseDetailsSerializer(
            course, context={"request": request}
        )
        return Response(
            {
                "message": "Enrolled in course",
                "data": serializer.data,
                "status": "success",
                "status_code": 200,
            },
            status=status.HTTP_200_OK,
        )
    except Course.DoesNotExist:
        return Response(
            {"message": "course not found", "status": "error", "status_code": 404},
            status=404,
        )
    except Exception as e:
        return Response(
            {"message": f"{str(e)}", "status": "error", "status_code": 400},
            status=400,
        )


def course_unregistration(request, course_id):
    try:
        course_exists = Course.objects.filter(id=course_id, is_deleted=False).exists()

        query = CoursePurchase.objects.filter(
            course=course_id,
            student=request.user.id,
            is_registered=True,
        )

        if course_exists and query.exists():
            course_purchase = query.first()
            course_purchase.is_registered = False
            course_purchase.save()
        elif not course_exists and query.exists():
            course_purchase = query.first()
            course_purchase.is_registered = False
            course_purchase.save()
        else:
            return Response(
                {
                    "message": "course purchase or course not found",
                    "status": "error",
                    "status_code": 404,
                },
                status=404,
            )
        return Response(
            {
                "message": "unregister for course",
                "status": "success",
                "status_code": 200,
            },
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        return Response(
            {"message": f"{str(e)}", "status": "error", "status_code": 400},
            status=400,
        )


def get_my_course(request, course_id):
    try:
        if course_id:
            student_details = CoursePurchase.objects.get(
                course=course_id,
                student=request.user.id,
                is_registered=True,
            )

            serializer = InstructorandCourseDetailsSerializer(
                student_details.course, context={"request": request}
            )

            return Response(
                {
                    "message": "student courses",
                    "data": serializer.data,
                    "status": "success",
                    "status_code": 200,
                },
                status=status.HTTP_200_OK,
            )
        else:
            query = CoursePurchase.objects.filter(
                student=request.user.id,
                is_registered=True,
            )

            enrolled_courses = query.all()

            if not enrolled_courses:
                return Response(
                    {
                        "message": "course not found",
                        "status": "error",
                        "status_code": 404,
                    },
                    status=404,
                )

            course_details = []

            for enrolled_course in enrolled_courses:
                serializer = InstructorandCourseDetailsSerializer(
                    enrolled_course.course, context={"request": request}
                )
                course_details.append(serializer.data)

            return Response(
                {
                    "message": "student courses",
                    "data": course_details,
                    "status": "success",
                    "status_code": 200,
                },
                status=status.HTTP_200_OK,
            )

    except CoursePurchase.DoesNotExist:
        return Response(
            {
                "message": "You haven't registered  for this course",
                "status": "error",
                "status_code": 404,
            },
            status=404,
        )
    except Course.DoesNotExist:
        return Response(
            {"message": "course not found", "status": "error", "status_code": 404},
            status=404,
        )
    except Exception as e:
        return Response(
            {"message": f"{str(e)}", "status": "error", "status_code": 400},
            status=400,
        )


def search_courses(request):
    try:
        search_query = request.query_params.get("s")

        search_result = Course.objects.filter(
            course_name__icontains=search_query, is_deleted=False
        ).all()

        if search_result is None:
            return Response(
                {"message": "no result found", "status": "error", "status_code": 404},
                status=404,
            )
        serializer = InstructorandCourseDetailsSerializer(
            search_result, many=True, context={"request": request}
        )
        return Response(
            {
                "message": "student courses",
                "data": serializer.data,
                "status": "success",
                "status_code": 200,
            },
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        return Response(
            {"message": f"{str(e)}", "status": "error", "status_code": 400},
            status=400,
        )
