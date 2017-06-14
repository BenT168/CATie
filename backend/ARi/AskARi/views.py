from django.contrib.auth.models import User
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.utils import jwt_decode_handler

from AskARi.models import Question
from AskARi.models import Question
from AskARi.serializers import QuestionSerializer
from courses.models import Course
from lecture.models import Lecture
from login.utils import can_access_course

pg_size = 25


def get_question(request, code, lectureURL, q_id):
    token = request.environ['HTTP_AUTHORIZATION']
    username = jwt_decode_handler(token)['username']
    access, resp = can_access_course(User.objects.get(username=username), code)
    if not access:
        return resp
    course = Course.objects.get(code)
    try:
        lecture = Lecture.objects.get(urlName=lectureURL, course=course)
    except Lecture.DoesNotExist:
        return HttpResponseNotFound('Lecture ' + lectureURL +
                                    'not found for course ' + code)
    question = Question.objects.get(onLecture=lecture, id_per_lecture=q_id)
    serializer = QuestionSerializer(question, many=False)
    
    return JsonResponse(serializer.data, safe=False)


# PRE: No arguments are None (for now). TODO: Add if-checks for Nones
@permission_classes((IsAuthenticated,))
@authentication_classes((TokenAuthentication,))
def get_questions(request, code, lectureURL, pg_no):
    # Get username from token
    token = request.environ['HTTP_AUTHORIZATION']
    username = jwt_decode_handler(token)['username']

    # Check if user can access provided course, access is true if so
    access, resp = can_access_course(User.objects.get(username=username), code)
    if not access:
        return resp

    # Get appropriate course object
    course = Course.objects.get(code)
    # Try to get appropriate lecture object
    try:
        lecture = Lecture.objects.get(urlName=lectureURL, course=course)
    except Lecture.DoesNotExist:
        return HttpResponseNotFound('Lecture ' + lectureURL +
                                    'not found for course ' + code)

    # Get all questions for specified lecture
    questions = Question.objects.get(onLecture=lecture)

    # Order questions by id
    questions = questions.order_by('id')

    # Retrieve only questions "on page pg_no"
    questions = questions[pg_size * pg_no: pg_size * (pg_no + 1)]

    serializer = QuestionSerializer(questions, many=True)

    return JsonResponse(serializer.data, safe=False)


@permission_classes((IsAuthenticated,))
@authentication_classes((TokenAuthentication,))
def get_questions_all(request, pg_no):
    # return get_questions(request, None, None, pg_no)
    return None


@permission_classes((IsAuthenticated,))
@authentication_classes((TokenAuthentication,))
def get_questions_course(request, code, pg_no):
    # return get_questions(request, code, None, pg_no)
    return None
