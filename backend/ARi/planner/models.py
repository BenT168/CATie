from django.db import models


class CalendarEvent(models.Model):
    username = models.CharField(max_length=10)
    title = models.CharField(max_length=60)
    start = models.DateTimeField()
    end = models.DateTimeField()
    body = models.CharField(max_length=150) # new field
    isDraggable = models.BooleanField()
    isResizable = models.BooleanField()

    def __str__(self):
        return self.title
