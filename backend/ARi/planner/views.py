from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CalendarEvent
from .serializers import CalendarEventSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.utils import jwt_decode_handler


@csrf_exempt
@permission_classes((IsAuthenticated,))
@authentication_classes((TokenAuthentication,))
def create_event(request):
    token = request.environ['HTTP_AUTHORIZATION']
    username = jwt_decode_handler(token)['username']
    user = User.objects.get(username=username)

    title = request.POST.get('title', None)
    start = request.POST.get('start', None)
    if start is None:
        start = ""
    end = request.POST.get('end', None)
    if end is None:
        end = ""

    CalendarEvent.objects.create(title=title, start=start, end=end)

    return HttpResponse("Event created successfully.")


class CalendarEventList(generics.ListCreateAPIView):
    queryset = CalendarEvent.objects.all()
    serializer_class = CalendarEventSerializer


class CalendarEventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CalendarEvent.objects.all()
    serializer_class = CalendarEventSerializer
