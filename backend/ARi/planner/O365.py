from O365 import Event, Schedule
import time

# the code below is tested and works perfectly

# should be real email and password corresponding to the user
e = ''
p = ''
authentication = (e, p)

schedule = Schedule(authentication)
bookings = []

try:
    result = schedule.getCalendars()
    # print('\nFetched calendars for', e, 'was successful:', result, '\n')
except:
    print('Login failed for', e, '\n')

calendars = schedule.calendars


# FORMATS
# subject = string
# startTime Example = '21 Nov 17 19 00' where Format = 'Day Month Year Hour Minutes'
# endTime Example = '21 Nov 17 21 00' where Format same as above
def createEvent(subject, startTime, endTime):
    ev = Event(auth=authentication, cal=calendars[0])
    ev.setSubject(subject)
    ev.setStart(time.strptime(startTime, '%d %b %y %H %M'))
    ev.setEnd(time.strptime(endTime, '%d %b %y %H %M'))
    return ev.create()


def filterByDate(dateTime):
    events = []
    date = dateTime.split('T')[0]
    print(date)
    for b in bookings:
        if b.get('Start') == dateTime:
            events.append(b.get('Subject'))
    return events


def generateDateTimesForGivenDate(date):
    date += 'T'
    dateTimes = []
    times = [for i in range(1, 23)]
    for t in times:
        date += t + ':00:00Z'
        dateTimes.append(date)


# Creates an event here for testing purposes
# test_event = createEvent('SusanTest', '21 Nov 17 19 00', '21 Nov 17 21 00')

for cal in calendars:
    try:
        result = cal.getEvents()
        # print('Got:', len(cal.events), 'events in total from given calendar\n')
    except:
        print('Failed to fetch events')

    for event in cal.events:
        # holds everything in json format to make it easily extractable using key-value dictionary matching.
        bookings.append(event.toJson())

print("--- UPCOMING EVENTS ---")
for b in bookings:
    print("Title:", b.get('Subject'))
    print("Start:", b.get('Start'))
    print("End:", b.get('End'))
    print()

dateTime = '2017-11-22T16:00:00Z'
a = filterByDate(dateTime)
print(a)
