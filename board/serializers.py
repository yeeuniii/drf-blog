from datetime import datetime

from rest_framework import serializers

from board import models
from board.models import Post


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ['id', 'content', 'nickname', 'date']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Like
        fields = ['id', 'nickname']


class PostSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Post
        exclude = ['content']


class PostCreateSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(default=datetime.now)
    like_count = serializers.IntegerField(default=0)

    class Meta:
        model = models.Post
        fields = ['id', 'title', 'content', 'nickname', 'date', 'like_count']

    def create(self, validated_data):
        validated_data['date'] = self.fields['date'].get_default()
        validated_data['like_count'] = self.fields['like_count'].get_default()
        return Post.objects.create(**validated_data)


class PostDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = models.Post
        fields = ['id', 'title', 'content', 'nickname', 'date', 'like_count', 'comments']

