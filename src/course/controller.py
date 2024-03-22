from rest_framework import status
from rest_framework.response import Response
from course.models import Course
from course.serializers import (
    CourseDetailsSerializer,
    CourseTutorRegistrationSerializer,
)
from tutor_account.models import Tutor


def update_course_count(id):
    # Update course count in tutor table
    query = Course.objects.filter(tutor=id, is_deleted=False)
    course_count = query.count()
    course = query.first()
    course.tutor.course_count = course_count
    course.tutor.save()


def register_tutor_course(request):
    try:
        tutor = Tutor.objects.get(account=request.user.id)
        request.data["tutor"] = tutor.id
        serializer = CourseTutorRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        update_course_count(tutor.id)
        return Response(
            {
                "message": "course added to the portal success",
                "data": serializer.data,
                "status": "success",
                "status_code": 201,
            },
            status=status.HTTP_201_CREATED,
        )
    except Tutor.DoesNotExist:
        return Response(
            {"message": "user not found", "status": "error", "status_code": 404},
            status=404,
        )
    except Exception as e:
        return Response(
            {"message": f"{str(e)}", "status": "error", "status_code": 400},
            status=400,
        )


def update_tutor_course(request, course_id):
    try:
        course_data = Course.objects.get(pk=course_id, is_deleted=False)
        request.data["tutor"] = course_data.tutor.id
        serializer = CourseTutorRegistrationSerializer(
            course_data, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        update_course_count(course_data.tutor.id)

        return Response(
            {
                "message": "course details updated success",
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


def delete_tutor_cource(request, course_id):
    try:
        course = Course.objects.get(pk=course_id, is_deleted=False)
        course.is_deleted = True
        course.save()
        update_course_count(course.tutor.id)
        return Response(
            {
                "message": "course deleted success",
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


def get_courses_details(request, course_id):
    try:
        if course_id:
            course = Course.objects.get(
                pk=request.parser_context.get("kwargs").get("course_id"),
                is_deleted=False,
            )
            serializer = CourseDetailsSerializer(course, context={"request": request})
        else:
            all_courses = Course.objects.filter(is_deleted=False).all()
            serializer = CourseDetailsSerializer(
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
