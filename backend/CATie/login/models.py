from django.db import models
# Create your models here.

from django.contrib.auth.models import User

from courses.models import Year, Course


class CATieProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    year = models.ForeignKey(Year)
    courses = models.ManyToManyField(Course)
    is_staff = models.BooleanField(default=True)

    def __str__(self):
        return "CATie Profile: " + self.user.username

    class Meta:
        verbose_name = 'CATie Profile'
        verbose_name_plural = 'CATie Profiles'
