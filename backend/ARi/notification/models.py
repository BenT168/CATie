from django.core.validators import RegexValidator
from django.db import models

from courses.models import Course
from login.models import ARiProfile


class Notification(models.Model):
    name = models.CharField(max_length=60)
    course = models.ForeignKey(Course)
    message = models.CharField(max_length=200)
    category = models.CharField(max_length=60)

    def __str__(self):
        return str(self.course.code) + ' from ' + self.name + ' Notification: ' + self.message

    def save(self, *args, **kwargs):
        super(Notification, self).save(*args, **kwargs)
