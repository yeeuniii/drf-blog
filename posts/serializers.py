from datetime import datetime

from rest_framework import serializers

from posts import models
from posts.models import Posting


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ['content', 'nickname', 'date']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Like
        fields = ['nickname']


class PostingSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Posting
        exclude = ['content']


class PostingCreateSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(default=datetime.now)
    like_count = serializers.IntegerField(default=0)

    class Meta:
        model = models.Posting
        fields = ['pk', 'title', 'content', 'nickname', 'date', 'like_count']

    def create(self, validated_data):
        validated_data['date'] = self.fields['date'].get_default()
        validated_data['like_count'] = self.fields['like_count'].get_default()
        return Posting.objects.create(**validated_data)

