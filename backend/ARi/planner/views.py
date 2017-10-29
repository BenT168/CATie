from django.shortcuts import render
from .models import CalendarEvent
from .serializers import CalendarEventSerializer
from rest_framework import generics

from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.utils import jwt_decode_handler

from courses.models import Course
from courses.serializers import CourseSerializer
from login.models import ARiProfile


# returns the courses codes someone is subscribed to for a given date.
@permission_classes((IsAuthenticated,))
@authentication_classes((TokenAuthentication,))
def get_courses_for_date(date):
    token = request.environ['HTTP_AUTHORIZATION']
    username = jwt_decode_handler(token)['username']
    user = User.objects.get(username=username)

    ari_profile = ARiProfile.objects.get(user=user)
    courses = ari_profile.courses.all().order_by('code')
    serializer = CourseSerializer(courses, many=True)

    # serializer.

    # TODO find the way to continue from here and get the courses on that date
    # TODO using the code pass it below and get the time of the course.


# returns the datetime of the provided course lectures to schedule them in the planner.
def get_course_dateTimes(code):
    course = Course.objects.get(code=code)
    dateTimes = [course.dateTime_1, course.dateTime_2]
    return dateTimes


# retuns the time of the course to displayed in the planner.
def get_course_time(code):
    course = Course.objects.get(code=code)
    # this is string parsing depending on the format we are using from here https://docs.djangoproject.com/en/1.9/ref/settings/#datetime-input-formats
    time1 = 1 # TODO
    time2 = 2 # TODO
    times = [time1, time2]
    return times


class CalendarEventList(generics.ListCreateAPIView):
    queryset = CalendarEvent.objects.all()
    serializer_class = CalendarEventSerializer


class CalendarEventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CalendarEvent.objects.all()
    serializer_class = CalendarEventSerializer
