from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseNotFound, HttpResponse, \
    HttpResponseForbidden

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.utils import jwt_decode_handler

from courses.models import Course
from lecture.models import Lecture, UserNotes
from lecture.serializers import LectureAndNotesSerializer
from login.models import ARiProfile
from login.utils import can_access_course


@permission_classes((IsAuthenticated,))
@authentication_classes((TokenAuthentication,))
def get_lecture(request, code, lectureURL):
    token = request.environ['HTTP_AUTHORIZATION']
    username = jwt_decode_handler(token)['username']
    user = User.objects.get(username=username)
    access, resp = can_access_course(user, code)
    if not access:
        return resp
    course = Course.objects.get(code=code)
    try:
        lecture = course.lecture_set.get(urlName=lectureURL)
    except Lecture.DoesNotExist:
        return HttpResponseNotFound("Invalid lecture URL.")

    profile = ARiProfile.objects.get(user=user)
    notes = UserNotes.objects.get_or_create(lecture=lecture, profile=profile)[0]

    serializer = LectureAndNotesSerializer(notes, many=False)
    return JsonResponse(serializer.data, safe=False)


@csrf_exempt
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


# THIS IS A STUB. IGNORE.
@permission_classes((IsAuthenticated,))
@authentication_classes((TokenAuthentication,))
def lecture_add_content(request):
    token = request.environ['HTTP_AUTHORIZATION']
    username = jwt_decode_handler(token)['username']
    user = User.objects.get(username=username)
    if not user.is_staff:
        return HttpResponseForbidden("Only staff may create lectures.")

    return HttpResponse("Stub. Ignore for now.")


