from rest_framework import serializers

from AskARi.models import Question, Comment


class CommentSerializer(serializers.ModelSerializer):
    poster = serializers.SlugRelatedField(source='poster.user',
                                          read_only=True,
                                          slug_field='username')
    question = serializers.SlugRelatedField(source='parent',
                                            read_only=True,
                                            slug_field='id_per_lecture')
    parent = serializers.SlugRelatedField(source='parent_comment',
                                          read_only=True,
                                          slug_field='id_per_question')
    id = serializers.IntegerField(source='id_per_question', min_value=1)

    class Meta:
        model = Comment
        fields = ('content', 'poster', 'score', 'question', 'id', 'parent')


class QuestionSerializer(serializers.ModelSerializer):
    lecture = serializers.SlugRelatedField(source='parent',
                                           read_only=True,
                                           slug_field='urlName')
    poster = serializers.SlugRelatedField(source='poster.user',
                                          read_only=True,
                                          slug_field='username')
    id = serializers.IntegerField(source='id_per_lecture', min_value=1)

    class Meta:
        model = Question
        fields = ('title', 'body', 'lecture', 'poster', 'id')


class QuestionFullSerializer(QuestionSerializer):
    comment_set = CommentSerializer(many=True)

    class Meta:
        model = Question
        fields = QuestionSerializer.Meta.fields + ('comment_set',)

# class ReplySerializer(serializers.ModelSerializer):
#     poster = serializers.SlugRelatedField(source='poster.user',
#                                           read_only=True,
#                                           slug_field='username')
#
#     class Meta:
#         abstract = True
#         model = Reply
#         fields = ('content', 'poster', 'score')
#
#
# class FollowUpSerializer(ReplySerializer):
#     comment = serializers.SlugRelatedField(source='parent',
#                                            read_only=True,
#                                            slug_field='id_per_parent')
#
#     class Meta:
#         model = Comment
#         fields = ReplySerializer.Meta.fields + ('comment',)
