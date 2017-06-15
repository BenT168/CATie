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

pg_size = 25

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


@permission_classes((IsAuthenticated,))
@authentication_classes((TokenAuthentication,))
def get_questions(request, code=None, lectureURL=None, pg_no=0):
    # Get username from token
    token = request.environ['HTTP_AUTHORIZATION']
    username = jwt_decode_handler(token)['username']
    user = User.objects.get(username=username)

    if code:
        # Check if user can access provided course, access is true if so
        access, resp = can_access_course(user, code)
        if not access:
            return resp

        # Get appropriate course object
        course = Course.objects.get(code=code)
        if lectureURL:
            # Try to get appropriate lecture object
            try:
                lecture = Lecture.objects.get(urlName=lectureURL, course=course)
            except Lecture.DoesNotExist:
                return HttpResponseNotFound('Lecture ' + lectureURL +
                                            'not found for course ' + code)
            # Get all questions for specified lecture
            questions = Question.objects.filter(onLecture=lecture)
        else:
            questions = Question.objects.none()
            lectures = Lecture.objects.filter(course=course)
            for lecture in lectures:
                questions = questions | Question.objects.filter(onLecture=lecture)
    else:
        # Get all questions when course not specified
        questions = Question.objects.none()

        # Get courses that user has access to
        ari_profile = ARiProfile.objects.get(user=user)
        courses = ari_profile.courses.all()

        for course in courses:
            lectures = Lecture.objects.filter(course=course)
            for lecture in lectures:
                questions = questions | Question.objects.filter(onLecture=lecture)

    # Order questions by id
    questions = questions.order_by('id')

    # Retrieve only questions on page "pg_no"
    questions = questions[pg_size * pg_no: pg_size * (pg_no + 1)]
    serializer = QuestionSerializer(questions, many=True)

    return JsonResponse(serializer.data, safe=False)


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

