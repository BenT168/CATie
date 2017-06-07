from django.http import JsonResponse
from rest_framework_jwt.utils import jwt_decode_handler


def get_courses(request):

    token = request.POST.get('token', None)
    username = jwt_decode_handler(token)['username']

    return JsonResponse({'course': 'default'})
