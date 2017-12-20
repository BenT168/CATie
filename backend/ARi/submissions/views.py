from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.utils import jwt_decode_handler
from django.contrib.auth.models import User
from backend.ARi.submissions.models import Submission
from django.http import JsonResponse
from backend.ARi.submissions.serializers import SubmissionSerializer


@permission_classes((IsAuthenticated,))
@authentication_classes((TokenAuthentication,))
def get_submissions(request):
    token = request.environ['HTTP_AUTHORIZATION']
    username = jwt_decode_handler(token)['username']
    user = User.objects.get(username=username)

    if user.is_staff:
        submissions = Submission.objects.all().order_by('code')

    serializer = SubmissionSerializer(submissions, many=True)

    return JsonResponse(serializer.data, safe=False)
