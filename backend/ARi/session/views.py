from django.http import JsonResponse, HttpResponseNotFound

# Create your views here.
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated

from courses.models import Course
from session.models import Session
from session.serializers import SessionSerializer


@permission_classes((IsAuthenticated,))
@authentication_classes((TokenAuthentication,))
def get_session(request, code, nameURL):
    try:
        course = Course.objects.get(code=code)
        session = course.session_set.get(urlSuffix=nameURL)
    except Course.DoesNotExist:
        return HttpResponseNotFound("Invalid course code.")
    except Session.DoesNotExist:
        return
    serializer = SessionSerializer(code, many=True)

    return JsonResponse(serializer.data, safe=False)