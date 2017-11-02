rom django.core.validators import RegexValidator
from django.db import models

from courses.models import Course
from notification.utils import reformat_for_url
from login.models import ARiProfile


class Notification(models.Model):
    urlSafe = RegexValidator(r'^[a-zA-Z0-9]*$', 'Only alphanumeric characters '
                                                'and \'-\' are allowed.')

    name = models.CharField(max_length=60)
    urlName = models.CharField(max_length=60, validators=[urlSafe],
                               default="", editable=False)
    course = models.ForeignKey(Course)
    category = models.CharField(max_length=60)

    def __str__(self):
        return str(self.course.code) + ' Lecture: ' + self.name

    def save(self, *args, **kwargs):
        if not self.urlName:
            self.urlName = reformat_for_url(self.name)
        super(Lecture, self).save(*args, **kwargs)

    class Meta:
        unique_together = (("urlName", "course"),)
