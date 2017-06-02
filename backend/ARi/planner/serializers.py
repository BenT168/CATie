from rest_framework import serializers
from .models import CalendarEvent

class CalendarEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarEvent
        fields = ('title', 'date', 'startTime', 'endTime', 'isDraggable', 'isResizable')