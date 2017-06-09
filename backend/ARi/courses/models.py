from django.contrib.auth.models import Group
from django.db import models


class Year(models.Model):
    number = models.IntegerField()
    group = models.OneToOneField(Group, unique=True)

    def __str__(self):
        return 'Year ' + str(self.number)
# if not hasattr(Group, 'parent'):
#    field = models.ForeignKey(Group, blank=True, null=True,
#                              related_name='children')
#    field.contribute_to_class(Group, 'parent')


class Course(models.Model):
    name = models.CharField(max_length=60)
    code = models.IntegerField()
    ofYear = models.ForeignKey(Year)
    group = models.OneToOneField(Group, unique=True)

    def __str__(self):
        return 'Course: ' + self.name


class Session(models.Model):
    name = models.CharField(max_length=60)
    course = models.ForeignKey(Course)
    video = models.URLField()


    def __str__(self):
        return 'Session: ' + self.name

