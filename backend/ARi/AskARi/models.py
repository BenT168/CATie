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
    parent = models.ForeignKey(Lecture)
    poster = models.ForeignKey(ARiProfile)
    id_per_lecture = models.PositiveIntegerField()

    def __str__(self):
        return 'Question ' + str(self.id_per_lecture) + ' by ' + \
               self.poster.user.username + ': ' + self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            self.id_per_lecture = next_id(self.__class__, self.parent,
                                          'id_per_lecture')
        super(Question, self).save(*args, **kwargs)

    class Meta:
        unique_together = (('parent', 'id_per_lecture'),)


class Comment(models.Model):
    content = models.TextField(max_length=4000)
    poster = models.ForeignKey(ARiProfile)
    score = models.IntegerField(default=0)
    id_per_question = models.PositiveIntegerField()
    parent = models.ForeignKey(Question)

    # Direct parent, null if top-level comment
    parent_comment = models.ForeignKey("Comment", blank=True,
                                       null=True, default=None)

    def __str__(self):
        return 'Comment ' + str(self.id_per_question) + ' by ' + \
               self.poster.user.username + ' on question: ' + \
               str(self.parent_id)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.id_per_question = next_id(self.__class__, self.parent,
                                           'id_per_question')
        super(Comment, self).save(*args, **kwargs)

    class Meta:
        unique_together = (('parent', 'id_per_question'),)


# class FollowUp(Reply):
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     parent_id = models.PositiveIntegerField()
#     parent = GenericForeignKey('content_type', 'parent_id')
#
#     def __str__(self):
#         return 'Reply ' + str(self.id_per_parent) + ' by ' + \
#                self.poster.user.username + ' to: ' + \
#                str(self.id_per_parent)
#
#     def save(self, *args, **kwargs):
#         if not self.pk:
#             self.id_per_parent = next_id(self.__class__, self.parent,
#                                          'id_per_parent')
#         super(FollowUp, self).save(*args, **kwargs)
#
#     class Meta:
#         unique_together = (('content_type', 'parent_id', 'id_per_parent'),)
