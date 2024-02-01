from rest_framework import serializers

from board import models
from board.models import Post


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ['id', 'post_id', 'content', 'nickname', 'date']
        read_only_fields = ['post_id', 'date']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Like
        fields = ['nickname']
        read_only_fields = ['post_id']


class PostSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Post
        exclude = ['content', 'password']


class PostCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = models.Post
        fields = ['id', 'title', 'content', 'nickname', 'password']

    def validate_password(self, value):
        if not value.isdigit() or len(value) != 4:
            raise serializers.ValidationError("invalid password: 비밀번호는 4자리 숫자")
        return value


class PostDetailSerializer(serializers.ModelSerializer):
    likes = LikeSerializer(many=True, read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = models.Post
        fields = ['id', 'title', 'content', 'nickname', 'password', 'date', 'like_count', 'likes']
        read_only_fields = ('nickname', 'date', 'like_count')
