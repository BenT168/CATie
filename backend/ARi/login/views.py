from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login


def login_user(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponse("Logged in successfully")
        else:
            return HttpResponseForbidden("Disabled user")
    else:
        return HttpResponseForbidden("Invalid login")
