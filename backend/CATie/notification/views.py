from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.utils import jwt_decode_handler

from courses.models import Course
from courses.serializers import CourseSerializer
from lecture.serializers import LectureManySerializer
from login.models import CATieProfile
from notification.models import Notification


@permission_classes((IsAuthenticated,))
@authentication_classes((TokenAuthentication,))
def get_notification(request, code,):
    token = request.environ['HTTP_AUTHORIZATION']
    username = jwt_decode_handler(token)['username']
    user = User.objects.get(username=username)
    access, resp = can_access_course(user, code)
    if user.is_staff:
        notification = Notification.objects.all().order_by('category')

    serializer = NotificationSerializer(notification, many=False)
    return JsonResponse(serializer.data, safe=False)


@csrf_exempt
@permission_classes((IsAuthenticated,))
@authentication_classes((TokenAuthentication,))
def create_notification(request):
    token = request.environ['HTTP_AUTHORIZATION']
    username = jwt_decode_handler(token)['username']
    user = User.objects.get(username=username)
    if not user.is_staff:
        return HttpResponseForbidden("Only staff may create notification.")

    name = request.POST.get('name', None)
    course_code = request.POST.get('code', None)
    course = Course.objects.get(code=course_code)
    message = request.POST.get('message', None)
    category = request.POST.get('category', None)

    Notification.objects.create(name=name, course=course, message=message, category=category)

    return HttpResponse("Notification created successfully.")
