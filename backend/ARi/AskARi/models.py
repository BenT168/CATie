from django.db import models

# Create your models here.
from courses.models import Course
from lecture.models import Lecture


class Question(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField(max_length=4000)
    ofCourse = models.ForeignKey(Course)
    lecture = models.ForeignKey(Lecture)

    def __str__(self):
        return 'Question ' + str(self.id) + ': ' + self.title
