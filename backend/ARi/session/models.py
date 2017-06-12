from django.db import models

from courses.models import Course


class Session(models.Model):
    urlSuffix = models.CharField(max_length=60, primary_key=True)
    name = models.CharField(max_length=60)
    course = models.ForeignKey(Course)
    video = models.URLField(default="")
    slides = models.URLField(default="")

    def __str__(self):
        return 'Session: ' + self.name
