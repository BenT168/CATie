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
    code = models.IntegerField(unique=True)

    # used by the planner app to schedule the specific day accordingly based on course hours
    # assuming that course happens twice a week in 2 different dates and hours.
    # from documentation on format: https://docs.djangoproject.com/en/1.9/ref/settings/#datetime-input-formats
    dateTime_1 = models.DateTimeField(auto_now=False, auto_now_add=False)
    dateTime_2 = models.DateTimeField(auto_now=False, auto_now_add=False)

    ofYear = models.ForeignKey(Year)
    group = models.OneToOneField(Group, unique=True)

    def __str__(self):
        return 'Course: ' + self.name

    def save(self, *args, **kwargs):
        creating = False
        if not self.pk:
            creating = True
        super(Course, self).save(*args, **kwargs)
        if creating:
            # Code only executed when first created
            from lecture.models import Lecture
            Lecture.objects.create(name="General", course=self)

