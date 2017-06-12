from django.core.validators import RegexValidator
from django.db import models

from courses.models import Course


class Session(models.Model):
    urlSafe = RegexValidator(r'^[a-zA-Z0-9]*$', 'Only alphanumeric characters '
                                                'and \'-\' are allowed.')
    name = models.CharField(max_length=60, validators=[urlSafe], unique=True,
                            primary_key=True)
    course = models.ForeignKey(Course)
    video = models.URLField(default="")
    slides = models.URLField(default="")

    def __str__(self):
        return 'Session: ' + self.name
