from django.db import models

# Create your models here.
from courses.models import Course
from lecture.models import Lecture
from login.models import ARiProfile

# TODO: Create abstract post class the others will inherit from.
# class Post(models.Model):


class Question(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField(max_length=4000)
    ofCourse = models.ForeignKey(Course)
    ofLecture = models.ForeignKey(Lecture)
    poster = models.ForeignKey(ARiProfile)

    def __str__(self):
        return 'Question ' + str(self.id) + ' by ' + \
               self.poster.user.username + ': ' + self.title


class Comment(models.Model):
    content = models.TextField(max_length=4000)
    onQuestion = models.ForeignKey(Question, null=True)
    poster = models.ForeignKey(ARiProfile)
    score = models.IntegerField()

    def __str__(self):
        return 'Comment ' + str(self.id) + ' by ' + self.poster.user.username\
            + ' on question: ' + str(self.onQuestion_id)


class FollowUp(models.Model):
    content = models.TextField(max_length=4000)
    onComment = models.ForeignKey(Comment)
    poster = models.ForeignKey(ARiProfile)
