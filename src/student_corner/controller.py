from course.models import Course
from rest_framework import status
from rest_framework.response import Response
from student_corner.models import CourseRegistration
from course.serializers import CourseDetailsSerializer, FullDetailsforEnrolledSerializer
from student_corner.serializers import RegisterForCourseSerializer


def update_student_count_and_cash_earned(course_id):
    student_count = CourseRegistration.objects.filter(
        enrolled_in=course_id, is_registered=True
    ).count()
    course = Course.objects.get(id=course_id, is_deleted=False)
    course.student_count = student_count
    course.tutor.money_earned += course.course_price
    course.tutor.save()
    course.save()


def course_registration(request, course_id):
    try:
        course = Course.objects.get(id=course_id, is_deleted=False)
        if CourseRegistration.objects.filter(
            enrolled_in=course_id, student_account=request.user.id, is_registered=True
        ).exists():
            raise Exception("You have already enrolled in course")

        if CourseRegistration.objects.filter(
            enrolled_in=course_id, student_account=request.user.id, is_registered=False
        ).exists():
            reg_course = CourseRegistration.objects.get(
                enrolled_in=course_id,
                student_account=request.user.id,
                is_registered=False,
            )
            reg_course.is_registered = True
            reg_course.save()
        else:
            data = {}

            data["enrolled_in"] = course_id
            data["student_account"] = request.user.id

            serializer = RegisterForCourseSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(fee_paid=course.course_price)
        update_student_count_and_cash_earned(course_id)
        return Response(
            {
                "message": "Enrolled in course",
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
        course = Course.objects.get(id=course_id, is_deleted=False)

        reg_course = CourseRegistration.objects.get(
            enrolled_in=course_id,
            student_account=request.user.id,
            is_registered=True,
        )
        if CourseRegistration.objects.filter(
            enrolled_in=course_id, student_account=request.user.id, is_registered=True
        ).exists():
            reg_course.is_registered = False
            reg_course.save()
        return Response(
            {
                "message": "Unregister for course",
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
    except CourseRegistration.DoesNotExist:
        return Response(
            {
                "message": "You haven't registred for this course",
                "status": "error",
                "status_code": 404,
            },
            status=404,
        )
    except Exception as e:
        return Response(
            {"message": f"{str(e)}", "status": "error", "status_code": 400},
            status=400,
        )


def get_my_course(request, course_id):
    try:
        if course_id:
            student_details = CourseRegistration.objects.get(
                enrolled_in=course_id,
                student_account=request.user.id,
                is_registered=True,
            )

            serializer = FullDetailsforEnrolledSerializer(
                student_details.enrolled_in, context={"request": request}
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
            query = CourseRegistration.objects.filter(
                student_account=request.user.id,
                is_registered=True,
            )

            enrolled_courses = query.all()

            course_details = []

            for enrolled_course in enrolled_courses:
                serializer = FullDetailsforEnrolledSerializer(
                    enrolled_course.enrolled_in, context={"request": request}
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

    except CourseRegistration.DoesNotExist:
        return Response(
            {
                "message": "You haven't registred for this course",
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

        search_result = Course.objects.filter(course_name__icontains=search_query).all()
        serializer = CourseDetailsSerializer(
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
