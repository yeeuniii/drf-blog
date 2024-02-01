from django.http import HttpResponseRedirect
from django.shortcuts import get_list_or_404,get_object_or_404
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from board.models import Post, Comment, Like
from board.serializers import PostSimpleSerializer, \
    PostCreateSerializer, PostDetailSerializer, \
    CommentSerializer, LikeSerializer


# Create your views here.


class PostsView(APIView):
    def get(self, request):
        posts = get_list_or_404(Post)
        post_serializer = PostSimpleSerializer(posts, many=True)
        return Response(post_serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        post_serializer = PostCreateSerializer(data=request.data)
        if post_serializer.is_valid():
            post_serializer.save()
            return Response("게시물 작성 성공", status=status.HTTP_201_CREATED)
        return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostView(APIView):
    def check_password(self, post, input_password):
        return input_password and post.password == input_password

    def handle_invliad_password(self, post, password):
        if not password:
            return Response("비밀번호 미입력", status=status.HTTP_400_BAD_REQUEST)
        return Response("비밀번호 불일치", status=status.HTTP_403_FORBIDDEN)

    def update_post(self, request, post_id, allow_partial=False):
        post = get_object_or_404(Post, id=post_id)
        post_serializer = PostDetailSerializer(post, data=request.data, partial=allow_partial)
        if not post_serializer.is_valid():
            return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        password = post_serializer.validated_data.get('password')
        if not self.check_password(post, password):
            return self.handle_invliad_password(post, password)
        post_serializer.save()
        return Response("게시물 수정 성공", status=status.HTTP_200_OK)

    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        post_serializer = PostDetailSerializer(post)
        return Response(post_serializer.data)

    def put(self, request, post_id):
        return self.update_post(request, post_id)

    def patch(self, request, post_id):
        return self.update_post(request, post_id, allow_partial=True)

    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        password = request.GET.get('password')
        if not self.check_password(post, password):
            return self.handle_invliad_password(post, password)
        post.delete()
        return Response("게시물 삭제 성공", status=status.HTTP_200_OK)


class CommentView(APIView):
    def get(self, request, post_id):
        comments = Comment.objects.filter(post_id=post_id)
        if not comments.exists():
            return Response("댓글 없음", status=status.HTTP_404_NOT_FOUND)
        comment_serializer = CommentSerializer(comments, many=True)
        return Response(comment_serializer.data, status=status.HTTP_200_OK)

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        comment_serializer = CommentSerializer(data=request.data)
        if not comment_serializer.is_valid():
            return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        comment_serializer.save(post_id=post)
        return Response("댓글 작성 성공", status=status.HTTP_201_CREATED)


class LikeView(APIView):
    def check_valid_like(self, nickname, post_id):
        return nickname and not Like.objects.filter(post_id=post_id).filter(nickname=nickname)

    def get(self, request, post_id):
        likes = get_list_or_404(Like, post_id=post_id)
        like_serializer = LikeSerializer(likes, many=True)
        return Response(like_serializer.data, status=status.HTTP_200_OK)

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like_serializer = LikeSerializer(data=request.data)
        if not like_serializer.is_valid():
            return Response(like_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if not self.check_valid_like(like_serializer.validated_data.get('nickname'), post_id):
            return Response("이미 좋아요 누름", status=status.HTTP_403_FORBIDDEN)
        post.like_count += 1
        post.save()
        like_serializer.save(post_id=post)
        return Response("좋아요 누르기 성공", status=status.HTTP_201_CREATED)

