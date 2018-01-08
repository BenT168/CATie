from rest_framework import serializers
from backend.ARi.submissions.models import Submission


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ('username', 'course', 'title', 'file', 'marked',
                  'grade', 'collected')
