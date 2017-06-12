from django.core.validators import RegexValidator
from django.db import models

from courses.models import Course
from session.utils import reformat_for_url


class Session(models.Model):
    urlSafe = RegexValidator(r'^[a-zA-Z0-9]*$', 'Only alphanumeric characters '
                                                'and \'-\' are allowed.')

    name = models.CharField(max_length=60)
    urlName = models.CharField(max_length=60, validators=[urlSafe],
                               primary_key=True, default="")
    course = models.ForeignKey(Course)
    video = models.URLField(default="")
    slides = models.URLField(default="")

    def __str__(self):
        return 'Session: ' + self.name

    def save(self, *args, **kwargs):
        if not self.urlName:
            self.urlName = reformat_for_url(self.name)
        super(Session, self).save(*args, **kwargs)
