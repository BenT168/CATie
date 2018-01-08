from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.utils import jwt_decode_handler
from O365 import Event, Schedule
import time

@csrf_exempt
@permission_classes((IsAuthenticated,))
@authentication_classes((TokenAuthentication,))
def create_event(request):
    token = request.environ['HTTP_AUTHORIZATION']
    username = jwt_decode_handler(token)['username']
    email = username + '@ic.ac.uk'
    password = request.POST.get('password', None)

    authentication = (email, password)
    schedule = Schedule(authentication)
    res = schedule.getCalendars()  # not used but essential for successful event creation.
    calendars = schedule.calendars
    ev = Event(auth=authentication, cal=calendars[0])

    subject = request.POST.get('title', None)
    startTime = request.POST.get('start', None)
    endTime = request.POST.get('end', None)
    body = request.POST.get('body', None)

    ev.setSubject(subject)
    ev.setStart(time.strptime(startTime, '%d %b %y %H %M'))
    ev.setEnd(time.strptime(endTime, '%d %b %y %H %M'))
    if body: ev.setBody(body)
    return ev.create()

    return HttpResponse("Event created successfully.")


# Returns an array that holds all the upcoming events for the provided user.
def get_events(request):
    token = request.environ['HTTP_AUTHORIZATION']
    username = jwt_decode_handler(token)['username']
    email = username + '@ic.ac.uk'
    password = request.POST.get('password', None)

    authentication = (email, password)
    schedule = Schedule(authentication)
    bookings = []

    try:
        result = schedule.getCalendars()
    # print('\nFetched calendars for', email, 'was successful:', result, '\n')
    except:
        print('Login failed for', email, '\n')

    calendars = schedule.calendars

    for cal in calendars:
        try:
            result = cal.getEvents()
            # print('Got:', len(cal.events), 'events in total from given calendar\n')
        except:
            print('Failed to fetch events')

        for event in cal.events:
            # holds everything in json format to make it easily extractable using key-value dictionary matching.
            bookings.append(event.toJson())

            return bookings
