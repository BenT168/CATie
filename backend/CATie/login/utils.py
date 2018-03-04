from django.http import HttpResponseNotFound, HttpResponseForbidden

from courses.models import Course
from login.models import CATieProfile


def can_access_course(user, code):
    try:
        profile = CATieProfile.objects.get(user=user)
        course = Course.objects.get(code=code)
    except CATieProfile.DoesNotExist:
        return False, HttpResponseNotFound("User does not have an CATieProfile.")
    except Course.DoesNotExist:
        return False, HttpResponseNotFound("Invalid course code.")

    return course in profile.courses.all(), \
        HttpResponseForbidden(user.username + ' does not take course ' + code)
