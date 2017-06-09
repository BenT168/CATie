from django.db import models
# Create your models here.

from django.contrib.auth.models import User

from courses.models import Year, Course


class ARiProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    year = models.OneToOneField(Year, unique=True)
    courses = models.ManyToManyField(Course)

    def __str__(self):
        return "ARiProfile: " + self.user.username
