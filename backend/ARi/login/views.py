from django.http import HttpResponseForbidden, JsonResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from rest_framework_jwt.settings import api_settings

from login.models import ARiProfile


@csrf_exempt
def login_user(request):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    username = request.POST.get('username', None)
    password = request.POST.get('password', None)

    if not password:
       return HttpResponseForbidden("Invalid login")

    user = authenticate(username=username, password=password)
    profile = None
    if user is not None:
        if user.is_active:
            login(request, user)
            if not user.is_staff:
                hasYear = False
                for g in request.user.groups.all():
                    if hasattr(g, 'year'):
                        profile = ARiProfile.objects.get_or_create(user=user,
                                                               year=g.year)[0]
                        hasYear = True
                        break
                if not hasYear:
                    return HttpResponseForbidden("Student does not have a "
                                                     "year.")
            for g in request.user.groups.all():
                if hasattr(g, 'course'):
                    profile.courses.add(g.course)

            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            return JsonResponse({'token': token, 'is_staff': user.is_staff})
        else:
            return HttpResponseForbidden("Disabled user")
    else:
        return HttpResponseForbidden("Invalid login")

