from rest_framework import status
from rest_framework.response import Response
from course.models import Course
from course.serializers import (
    CourseDetailsSerializer,
    CourseTutorRegistrationSerializer,
)


def registerTutorCourse(request):
    try:
        request.data["tutor"] = request.user.id
        serializer = CourseTutorRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "message": "course added to the portal success",
                "status": "success",
                "status_code": 201,
            },
            status=status.HTTP_201_CREATED,
        )
    except Exception as e:
        return Response(
            {"message": f"{str(e)}", "status": "error", "status_code": 400},
            status=400,
        )


def updateTutorCourse(request, course_id):
    try:
        course_data = Course.objects.get(pk=course_id, is_deleted=False)
        serializer = CourseTutorRegistrationSerializer(
            course_data, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "message": "course details updated success",
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


def deleteTutorCource(request, course_id):
    try:
        course = Course.objects.get(pk=course_id)
        course.is_deleted = True
        course.save()
        return Response(
            {
                "message": "course deleted success",
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


def getCoursesDetails(request, course_id):
    try:
        if course_id:
            course = Course.objects.get(
                pk=request.parser_context.get("kwargs").get("course_id"),
                is_deleted=False,
            )
            serializer = CourseDetailsSerializer(course)
        else:
            all_courses = Course.objects.filter(is_deleted=False).all()
            serializer = CourseDetailsSerializer(all_courses, many=True)

        return Response(
            {
                "message": "course details succcess",
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
