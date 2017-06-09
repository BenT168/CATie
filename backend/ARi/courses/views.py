from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.utils import jwt_decode_handler

from courses.serializers import CourseSerializer
from login.models import ARiProfile


@permission_classes((IsAuthenticated,))
@authentication_classes((TokenAuthentication,))
def get_courses(request):

    username = request.user

    #token = request.get('token', None)
    #username = jwt_decode_handler(token)['username']
    user = User.objects.get(username=username)
    ari_profile = ARiProfile.objects.get(user=user)
    courses = ari_profile.courses.all()

    serializer = CourseSerializer(courses, many=True)

    return JsonResponse(serializer.data, safe=False)