from datetime import datetime

from rest_framework import serializers
from rest_framework.fields import empty

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
        exclude = ['content', 'password']


class PostCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    date = serializers.DateTimeField(default=datetime.now)
    like_count = serializers.IntegerField(default=0)

    class Meta:
        model = models.Post
        fields = ['id', 'title', 'content', 'nickname', 'password', 'date', 'like_count']


    def create(self, validated_data):
        validated_data['date'] = self.fields['date'].get_default()
        validated_data['like_count'] = self.fields['like_count'].get_default()
        return Post.objects.create(**validated_data)

    def validate_password(self, value):
        if not value.isdigit() or len(value) != 4:
            raise serializers.ValidationError()
        return value


class PostDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
    date = serializers.DateTimeField(required=False)
    like_count = serializers.IntegerField(required=False)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = models.Post
        fields = ['id', 'title', 'content', 'nickname', 'password', 'date', 'like_count', 'comments', 'likes']
