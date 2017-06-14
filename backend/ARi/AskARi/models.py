from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Create your models here.
from AskARi.utils import next_id
from lecture.models import Lecture
from login.models import ARiProfile


class Question(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField(max_length=4000)
    onLecture = models.ForeignKey(Lecture)
    poster = models.ForeignKey(ARiProfile)
    id_per_lecture = models.IntegerField()

    def __str__(self):
        return 'Question ' + str(self.id_per_lecture) + ' by ' + \
               self.poster.user.username + ': ' + self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            self.id_per_lecture = next_id(self.__class__, self.onLecture,
                                          'id_per_lecture')
        super(Question, self).save(*args, **kwargs)

    class Meta:
        unique_together = (('onLecture', 'id_per_lecture'),)


class Reply(models.Model):
    content = models.TextField(max_length=4000)
    poster = models.ForeignKey(ARiProfile)
    score = models.IntegerField()
    id_per_parent = models.PositiveIntegerField()

    class Meta:
        abstract = True


class Comment(Reply):
    onQuestion = models.ForeignKey(Question)

    def __str__(self):
        return 'Comment ' + str(self.id_per_parent) + ' by ' + \
               self.poster.user.username + ' on question: ' + \
               str(self.onQuestion_id)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.id_per_lecture = next_id(self.__class__, self.onQuestion,
                                          'id_per_parent')
        super(Comment, self).save(*args, **kwargs)

    class Meta:
        unique_together = (('onQuestion', 'id_per_parent'),)


class FollowUp(Reply):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    parent_id = models.PositiveIntegerField()
    follow_up_to = GenericForeignKey('content_type', 'parent_id')

    def __str__(self):
        return 'Reply ' + str(self.id_per_parent) + ' by ' + \
               self.poster.user.username + ' to: ' + \
               str(self.id_per_parent)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.id_per_lecture = next_id(self.__class__, self.follow_up_to,
                                          'id_per_parent')
        super(FollowUp, self).save(*args, **kwargs)

    class Meta:
        unique_together = (('content_type', 'parent_id', 'id_per_parent'),)
