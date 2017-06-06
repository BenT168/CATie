from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login

from login.models import ARiUser


def login_user(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            ARiUser.objects.get_or_create(user=user)
            return HttpResponse("Logged in successfully")
        else:
            return HttpResponseForbidden("Disabled user")
    else:
        return HttpResponseForbidden("Invalid login")
