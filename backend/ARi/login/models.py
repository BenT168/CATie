from django.db import models

# Create your models here.

from django.contrib.auth.models import User


class ARiUser(models.Model):
    """User profile.  Contains some basic configurable settings"""
    user = models.OneToOneField(User)
