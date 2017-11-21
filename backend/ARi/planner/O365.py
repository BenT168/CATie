from O365 import Event, Schedule
import time

email = ' '
password = ' '


# Returns an array that holds all the upcoming events for the provided user.
def getAllUpcomingEventsForUser(email, password):
    schedule = Schedule((email, password))
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


# FORMATS
# subject = string
# startTime Example = '21 Nov 17 19 00' where Format = 'Day Month Year Hour Minutes'
# endTime Example = '21 Nov 17 21 00' where Format same as above
def createEvent(email, password, subject, startTime, endTime):
    authentication = (email, password)
    schedule = Schedule(authentication)
    res = schedule.getCalendars()  # not used but essential for successful event creation.
    calendars = schedule.calendars
    ev = Event(auth=authentication, cal=calendars[0])
    ev.setSubject(subject)
    ev.setStart(time.strptime(startTime, '%d %b %y %H %M'))
    ev.setEnd(time.strptime(endTime, '%d %b %y %H %M'))
    return ev.create()


# Filters the list of upcoming events for user given a date
# DATE FORMAT: '2017-12-06'
# Note: Currently does not support filtering for events that are occurring in other hours than whole hours.
def filterByDate(date, bookings):
    events = []
    dateTimes = generateDateTimesForGivenDate(date)
    for b in bookings:
        for d in dateTimes:
            try:
                if b.get('Start') == d:
                    events.append(b)
            except:
                print("No events on given date", date)
    return events


# Helper function used by filterByDate to concat all possible hours of a given date.
# Note: Currently does not support filtering for events that are occurring in other hours than whole hours.
def generateDateTimesForGivenDate(dateGiven):
    dateTimes = []
    times = [i for i in range(0, 24)]
    for t in times:
        date = dateGiven
        if t < 10: date += 'T0' + str(t) + ':00:00Z'
        else: date += 'T' + str(t) + ':00:00Z'
        dateTimes.append(date)
    return dateTimes


# Display all upcoming events
def displayEvents(bookings, date=None):
    if date:
        bookings = filterByDate(date, bookings)
        print("--- UPCOMING EVENTS FOR:", date, "---")
        for b in bookings:
            print("Title:", b.get('Subject'))
            print("Start:", b.get('Start'))
            print("End:", b.get('End'))
            print()
    else:
        print("--- ALL UPCOMING EVENTS ---")
        for b in bookings:
            print("Title:", b.get('Subject'))
            print("Start:", b.get('Start'))
            print("End:", b.get('End'))
            print()


# Testing
# CURRENT STATE: EVERYTHING WORKS.
bookings = getAllUpcomingEventsForUser(email, password)
# displayEvents(bookings)
# createEvent(email, password, "Susan test", "30 Nov 17 19 00", "30 Nov 17 21 00")
# displayEvents(bookings)
displayEvents(bookings, '2017-12-06')
