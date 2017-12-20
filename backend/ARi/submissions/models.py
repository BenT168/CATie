from django.db import models
from backend.ARi.courses.models import Course
from django.core.validators import MaxValueValidator, MinValueValidator


class Submission(models.Model):
    username = models.CharField(max_length=10)
    course = models.ForeignKey(Course)
    title = models.CharField(max_length=60)
    marked = models.BooleanField(default=False)
    grade = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(0)])
    collected = models.BooleanField(default=False)
