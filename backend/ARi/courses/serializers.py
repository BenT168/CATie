from rest_framework import serializers

from courses.models import Course
from session.models import Session


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('code', 'name')


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ('name', 'video', 'slides')
