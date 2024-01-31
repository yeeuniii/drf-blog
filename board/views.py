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
        queryset = get_list_or_404(Post)
        serializer_class = PostSimpleSerializer(data=queryset, many=True)
        serializer_class.is_valid()
        return Response(serializer_class.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer_class = PostCreateSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)


class PostView(APIView):
    def check_password(self, posting, input_password):
        return posting.password == input_password

    def update_post(self, request, post_id, allow_partial=False):
        posting = get_object_or_404(Post, id=post_id)
        serializer_class = PostDetailSerializer(posting, data=request.data, partial=allow_partial)
        if not serializer_class.is_valid():
            return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
        password = serializer_class.validated_data['password']
        if not password:
            return Response("비밀번호 미입력", status=status.HTTP_400_BAD_REQUEST)
        if not self.check_password(posting, input_password=password):
            return Response("비밀번호 불일치", status=status.HTTP_403_FORBIDDEN)
        serializer_class.save()
        return Response(serializer_class.data, status=status.HTTP_200_OK)

    def get(self, request, post_id):
        posting = get_object_or_404(Post, id=post_id)
        serializer_class = PostDetailSerializer(posting)
        return Response(serializer_class.data)

    def put(self, request, post_id):
        return self.update_post(request, post_id)

    def patch(self, request, post_id):
        return self.update_post(request, post_id, allow_partial=True)

    def delete(self, request, post_id):
        posting = get_object_or_404(Post, id=post_id)
        password = request.GET.get('password')
        if not password:
            return Response("비밀번호 미입력", status=status.HTTP_400_BAD_REQUEST)
        if not self.check_password(posting, input_password=password):
            return Response("비밀번호 불일치", status=status.HTTP_403_FORBIDDEN)
        posting.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentView(APIView):
    def get(self, request, post_id):
        comments = Comment.objects.filter(post_id=post_id)
        if not comments.exists():
            return Response("댓글 없음", status=status.HTTP_404_NOT_FOUND)
        comment_serializer = CommentSerializer(data=comments, many=True)
        comment_serializer.is_valid()
        return Response(comment_serializer.data, status=status.HTTP_200_OK)

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        comment_serializer = CommentSerializer(data=request.data, context={'post_id': post_id})
        if comment_serializer.is_valid():
            comment_serializer.save(post_id=post)
            return HttpResponseRedirect(reverse('board:post', kwargs={'post_id': post_id}))
        return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LikeView(APIView):
    def get(self, request, post_id):
        likes = get_list_or_404(Like, post_id=post_id)
        like_serializer = LikeSerializer(data=likes, many=True)
        like_serializer.is_valid()
        return Response(like_serializer.data, status=status.HTTP_200_OK)

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)

        like_serializer = LikeSerializer(data=request.data, context={'post_id': post_id})
        if not like_serializer.is_valid():
            return Response(like_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        password = like_serializer.validated_data['nickname']
        like = Like.objects.filter(post_id=post_id).filter(nickname=password)
        if like:
            return Response("이미 좋아요 누름", status=status.HTTP_403_FORBIDDEN)
        post.like_count += 1
        post.save()
        like_serializer.save(post_id=post)
        return HttpResponseRedirect(reverse('board:post', kwargs={'post_id': post_id}))

