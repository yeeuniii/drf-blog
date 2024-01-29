from datetime import datetime

from rest_framework import serializers

from posts import models
from posts.models import Posting


class PostingSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(default=datetime.now)
    like_count = serializers.IntegerField(default=0)

    class Meta:
        model = models.Posting
        fields = ['pk', 'title', 'content', 'nickname', 'date', 'like_count']

    def create(self, validated_data):
        validated_data['date'] = self.fields['date'].get_default()
        validated_data['like_count'] = self.fields['like_count'].get_default()
        return Posting.objects.create(**validated_data)


class CommentSerializer(serializers.ModelSerializer):
    posting = PostingSerializer()

    class Meta:
        model = models.Comment
        fields = ['posting_id', 'content', 'nickname', 'date']


class LikeSerializer(serializers.ModelSerializer):
    posting = PostingSerializer()

    class Meta:
        model = models.Like
        fields = ['posting_id', 'nickname']
