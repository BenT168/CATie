from rest_framework import serializers

from login.models import CATieProfile


# Unused and broken
# class CATieProfileSerializer(serializers.ModelSerializer):
#     user = serializers.SlugRelatedField(slug_field='username')
#
#     class Meta:
#         model = CATieProfile
#         fields = ('user',)
