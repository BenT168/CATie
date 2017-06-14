from django.http import HttpResponseNotFound, HttpResponseForbidden

from courses.models import Course


def can_access_course(user, code):
    try:
        course = Course.objects.get(code=code)
    except:
        return False, HttpResponseNotFound("Invalid course code.")

    return course.group in user.groups, \
        HttpResponseForbidden(user.username + ' does not take course ' + code)
