from rest_framework import serializers

from AskARi.models import Question, Reply, Comment


class QuestionSerializer(serializers.ModelSerializer):
    lecture = serializers.SlugRelatedField(source='onLecture',
                                           read_only=True,
                                           slug_field='urlName')
    poster = serializers.SlugRelatedField(source='poster.user',
                                          read_only=True,
                                          slug_field='username')

    class Meta:
        model = Question
        fields = ('title', 'body', 'lecture', 'poster')


class ReplySerializer(serializers.ModelSerializer):
    poster = serializers.SlugRelatedField(source='poster.user',
                                          read_only=True,
                                          slug_field='username')

    class Meta:
        abstract = True
        model = Reply
        fields = ('content', 'poster', 'score')


class CommentSerializer(ReplySerializer):
    question = serializers.SlugRelatedField(source='onQuestion',
                                            read_only=True,
                                            slug_field='id_per_lecture')

    class Meta:
        model = Comment
        fields = ReplySerializer.Meta.fields + ('question',)


class FollowUpSerializer(ReplySerializer):
    comment = serializers.SlugRelatedField(source='follow_up_to',
                                           read_only=True,
                                           slug_field='id_per_parent')

    class Meta:
        model = Comment
        fields = ReplySerializer.Meta.fields + ('comment',)
