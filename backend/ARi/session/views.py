from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseNotFound, HttpResponse, \
    HttpResponseForbidden

# Create your views here.
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.utils import jwt_decode_handler

from courses.models import Course
from session.models import Session
from session.serializers import SessionSerializer
from session.utils import reformat_for_url


@permission_classes((IsAuthenticated,))
@authentication_classes((TokenAuthentication,))
def get_session(request, code, name):
    try:
        course = Course.objects.get(code=code)
        session = course.session_set.get(name=name)
    except Course.DoesNotExist:
        return HttpResponseNotFound("Invalid course code.")
    except Session.DoesNotExist:
        return HttpResponseNotFound("Invalid session URL.")

    serializer = SessionSerializer(session, many=True)
    return JsonResponse(serializer.data, safe=False)


@permission_classes((IsAuthenticated,))
@authentication_classes((TokenAuthentication,))
def create_session(request):
    token = request.environ['HTTP_AUTHORIZATION']
    username = jwt_decode_handler(token)['username']
    user = User.objects.get(username=username)
    if not user.is_staff:
        return HttpResponseForbidden("Only staff may create sessions.")

    name = request.POST.get('name', None)
    course_code = request.POST.get('code', None)
    video = request.POST.get('video', None)
    slides = request.POST.get('slides', None)

    name_as_url = reformat_for_url(name)
    try:
        course = Course.objects.get(code=course_code)
    except Course.DoesNotExist:
        return HttpResponseNotFound("Creating session in invalid course.")

    Session.objects.create(name=name_as_url, course=course, video=video,
                           slides=slides)

    return HttpResponse("Session created successfully.")


@permission_classes((IsAuthenticated,))
@authentication_classes((TokenAuthentication,))
def session_add_content(request):
    token = request.environ['HTTP_AUTHORIZATION']
    username = jwt_decode_handler(token)['username']
    user = User.objects.get(username=username)
    if not user.is_staff:
        return HttpResponseForbidden("Only staff may create sessions.")

    return HttpResponse("Stub. Ignore for now.")


