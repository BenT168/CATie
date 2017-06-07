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

    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            ARiProfile.objects.get_or_create(user=user)

            payload = jwt_payload_handler(user)
            return JsonResponse({'token': jwt_encode_handler(payload)})
        else:
            return HttpResponseForbidden("Disabled user")
    else:
        return HttpResponseForbidden("Invalid login")
