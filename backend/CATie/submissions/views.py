from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.utils import jwt_decode_handler
from django.contrib.auth.models import User
from backend.ARi.submissions.models import Submission
from backend.ARi.courses.models import Course
from backend.ARi.submissions.serializers import SubmissionSerializer
from django.http import JsonResponse, HttpResponseNotFound, HttpResponse


# Stuff should create submissions like assignments, coursework etc giving the title, the type of file and the size
# required.  Then a student should submit the required file.
@permission_classes((IsAuthenticated,))
@authentication_classes((TokenAuthentication,))
def create_submissions(request):
    token = request.environ['HTTP_AUTHORIZATION']
    username = jwt_decode_handler(token)['username']
    user = User.objects.get(username=username)

    if user.is_staff:
        course = request.POST.get('course', None)
        if course is None:
            slides = ""
        try:
            course = Course.objects.get(code=course)
        except Course.DoesNotExist:
            return HttpResponseNotFound("Creating submission for invalid course.")

        title = request.POST.get('title', None)
        file = request.POST.get('file', None)
        dateTime = request.POST.get('dateTime', None)
        marked = request.POST.get('marked', None)
        grade = request.POST.get('grade', None)
        collected = request.POST.get('collected', None)

        Submission.objects.create(username=user, course=course, title=title,
                                  file=file, dateTime=dateTime, marked=marked,
                                  grade=grade, collected=collected)

    return HttpResponse("Assignment submission created successfully.")


# This should be used by stuff to get all submissions for a specific resource.
@permission_classes((IsAuthenticated,))
@authentication_classes((TokenAuthentication,))
def get_submissions(request):
    token = request.environ['HTTP_AUTHORIZATION']
    username = jwt_decode_handler(token)['username']
    user = User.objects.get(username=username)

    if user.is_staff:
        submissions = Submission.objects.all().order_by('code')

    serializer = SubmissionSerializer(submissions, many=True)

    return JsonResponse(serializer.data, safe=False)


