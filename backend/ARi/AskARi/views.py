from django.contrib.auth.models import User
from django.http import HttpResponseNotFound, JsonResponse, HttpResponse
from django.shortcuts import render


# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.utils import jwt_decode_handler

from AskARi.models import Question
from AskARi.serializers import QuestionSerializer
from courses.models import Course
from lecture.models import Lecture
from login.models import ARiProfile
from login.utils import can_access_course


@permission_classes((IsAuthenticated,))
@authentication_classes((TokenAuthentication,))
def get_question(request, code, lectureURL, q_id):
    token = request.environ['HTTP_AUTHORIZATION']
    username = jwt_decode_handler(token)['username']
    access, resp = can_access_course(User.objects.get(username=username), code)
    if not access:
        return resp
    course = Course.objects.get(code=code)
    try:
        lecture = Lecture.objects.get(urlName=lectureURL, course=course)
    except Lecture.DoesNotExist:
        return HttpResponseNotFound('Lecture ' + lectureURL +
                                    'not found for course ' + code)
    question = Question.objects.get(onLecture=lecture, id_per_lecture=q_id)
    serializer = QuestionSerializer(question, many=False)

    return JsonResponse(serializer.data, safe=False)


def get_questions(request, code, lectureURL, pg_no):
    return None


def get_questions_all(request, pg_no):
    return get_questions(request, None, None, pg_no)


def get_questions_course(request, code, pg_no):
    return get_questions(request, code, None, pg_no)


@csrf_exempt
@permission_classes((IsAuthenticated,))
@authentication_classes((TokenAuthentication,))
def create_question(request):
    token = request.environ['HTTP_AUTHORIZATION']
    username = jwt_decode_handler(token)['username']
    user = User.objects.get(username=username)
    profile = ARiProfile.objects.get(user=user)
    course_code = request.POST.get('code', None)
    access, resp = can_access_course(user, course_code)
    if not access:
        return resp
    course = Course.objects.get(code=course_code)
    lectureURL = request.POST.get('lecture', None)
    try:
        lecture = Lecture.objects.get(course=course, urlName=lectureURL)
    except Lecture.DoesNotExist:
        return HttpResponseNotFound("Course " + course_code + " does not have a"
                                    " lecture at " + str(lectureURL))
    title = request.POST.get('title', None)
    body = request.POST.get('body', None)
    Question.objects.create(title=title, body=body, onLecture=lecture,
                            poster=profile)

    return HttpResponse("Question created successfully")
