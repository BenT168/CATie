from rest_framework import serializers

from lecture.models import Lecture


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ('name', 'video', 'slides')
