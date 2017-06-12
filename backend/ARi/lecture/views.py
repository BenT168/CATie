from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseNotFound, HttpResponse, \
    HttpResponseForbidden

# Create your views here.
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.utils import jwt_decode_handler

from courses.models import Course
from lecture.models import Lecture
from lecture.serializers import LectureSerializer
from lecture.utils import reformat_for_url


@permission_classes((IsAuthenticated,))
@authentication_classes((TokenAuthentication,))
def get_lecture(request, code, nameURL):
    try:
        course = Course.objects.get(code=code)
        lecture = course.lecture_set.get(urlName=nameURL)
    except Course.DoesNotExist:
        return HttpResponseNotFound("Invalid course code.")
    except Lecture.DoesNotExist:
        return HttpResponseNotFound("Invalid lecture URL.")

    serializer = LectureSerializer(lecture, many=False)
    return JsonResponse(serializer.data, safe=False)


@permission_classes((IsAuthenticated,))
@authentication_classes((TokenAuthentication,))
def create_lecture(request):
    token = request.environ['HTTP_AUTHORIZATION']
    username = jwt_decode_handler(token)['username']
    user = User.objects.get(username=username)
    if not user.is_staff:
        return HttpResponseForbidden("Only staff may create lectures.")

    name = request.POST.get('name', None)
    course_code = request.POST.get('code', None)
    video = request.POST.get('video', None)
    if video is None:
        video = ""
    slides = request.POST.get('slides', None)
    if slides is None:
        slides = ""
    try:
        course = Course.objects.get(code=course_code)
    except Course.DoesNotExist:
        return HttpResponseNotFound("Creating lecture in invalid course.")

    Lecture.objects.create(name=name, course=course, video=video,
                           slides=slides)

    return HttpResponse("Lecture created successfully.")


@permission_classes((IsAuthenticated,))
@authentication_classes((TokenAuthentication,))
def lecture_add_content(request):
    token = request.environ['HTTP_AUTHORIZATION']
    username = jwt_decode_handler(token)['username']
    user = User.objects.get(username=username)
    if not user.is_staff:
        return HttpResponseForbidden("Only staff may create lectures.")

    return HttpResponse("Stub. Ignore for now.")


