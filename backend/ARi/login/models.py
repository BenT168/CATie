from django.db import models
# Create your models here.

from django.contrib.auth.models import User
from courses.models import Year


class ARiProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    yearGroup = models.ForeignKey(Year)
