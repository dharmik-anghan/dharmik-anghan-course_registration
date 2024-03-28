from course.models import Course
from django.db import transaction
from rest_framework import status
from instructor.models import Instructor
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from course.serializers import (
    GetCourseSerializer,
    RegisterCourseSerializer,
)


@transaction.atomic
def update_course_count(instructor_id):
    # Update course count in tutor table
    course_count = Course.objects.filter(
        instructor=instructor_id, is_deleted=False
    ).count()
    instructor = Instructor.objects.get(id=instructor_id)
    instructor.course_count = course_count
    instructor.save()


def register_for_course(request):
    try:
        instructor = Instructor.objects.get(instructor=request.user.id)
        request.data["instructor"] = instructor.id
        serializer = RegisterCourseSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            serializer.save()
            update_course_count(instructor.id)

        return Response(
            {
                "message": "course added to the portal success",
                "data": serializer.data,
                "status": "success",
                "status_code": 201,
            },
            status=status.HTTP_201_CREATED,
        )
    except Instructor.DoesNotExist or ObjectDoesNotExist:
        return Response(
            {"message": "user not found", "status": "error", "status_code": 404},
            status=404,
        )
    except Exception as e:
        return Response(
            {"message": f"{str(e)}", "status": "error", "status_code": 400},
            status=400,
        )


def update_course(request, course_id):
    try:
        course_data = Course.objects.get(pk=course_id, is_deleted=False)
        serializer = RegisterCourseSerializer(
            course_data, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "message": "course details updated success",
                "data": serializer.data,
                "status": "success",
                "status_code": 200,
            },
            status=status.HTTP_200_OK,
        )
    except Course.DoesNotExist or ObjectDoesNotExist:
        return Response(
            {"message": "course not found", "status": "error", "status_code": 404},
            status=404,
        )
    except Exception as e:
        return Response(
            {"message": f"{str(e)}", "status": "error", "status_code": 400},
            status=400,
        )


def delete_cource(request, course_id):
    try:
        course = Course.objects.get(pk=course_id, is_deleted=False)
        course.is_deleted = True
        course.save()
        update_course_count(course.instructor.id)
        return Response(
            {
                "message": "course deleted success",
                "status": "success",
                "status_code": 200,
            },
            status=status.HTTP_200_OK,
        )
    except Course.DoesNotExist or ObjectDoesNotExist:
        return Response(
            {"message": "course not found", "status": "error", "status_code": 404},
            status=404,
        )
    except Exception as e:
        return Response(
            {"message": f"{str(e)}", "status": "error", "status_code": 400},
            status=400,
        )


def get_courses_details(request, course_id):
    try:
        user = request.user
        instructor_info = Instructor.objects.get(instructor=user)
        if course_id:
            course = Course.objects.get(
                instructor=instructor_info,
                pk=course_id,
                is_deleted=False,
            )
            serializer = GetCourseSerializer(course, context={"request": request})
        else:
            all_courses = Course.objects.filter(
                instructor=instructor_info, is_deleted=False
            ).all()
            serializer = GetCourseSerializer(
                all_courses, context={"request": request}, many=True
            )

        return Response(
            {
                "message": "course details succcess",
                "data": serializer.data,
                "status": "success",
                "status_code": 200,
            },
            status=status.HTTP_200_OK,
        )
    except Course.DoesNotExist or ObjectDoesNotExist:
        return Response(
            {"message": "course not found", "status": "error", "status_code": 404},
            status=404,
        )
    except Exception as e:
        return Response(
            {"message": f"{str(e)}", "status": "error", "status_code": 400},
            status=400,
        )
