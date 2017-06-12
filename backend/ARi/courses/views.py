from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.utils import jwt_decode_handler

from courses.models import Course
from courses.serializers import CourseSerializer
from session.serializers import SessionSerializer
from login.models import ARiProfile


@permission_classes((IsAuthenticated,))
@authentication_classes((TokenAuthentication,))
def get_courses(request):
    token = request.environ['HTTP_AUTHORIZATION']
    username = jwt_decode_handler(token)['username']
    user = User.objects.get(username=username)
    if user.is_staff:
        courses = Course.objects.all()
    else:
        ari_profile = ARiProfile.objects.get(user=user)
        courses = ari_profile.courses.all()
    serializer = CourseSerializer(courses, many=True)

    return JsonResponse(serializer.data, safe=False)

@permission_classes((IsAuthenticated,))
@authentication_classes((TokenAuthentication,))
def get_sessions(request, code):
    course = Course.objects.get(code=code)
    sessions = course.session_set.all()

    serializer = SessionSerializer(sessions, many=True)

    return JsonResponse(serializer.data, safe=False)

