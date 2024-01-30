from django.http import HttpResponseRedirect
from django.shortcuts import get_list_or_404, get_object_or_404
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from board.models import Post
from board.serializers import PostSimpleSerializer, PostCreateSerializer, PostDetailSerializer, PostPasswordSerializer


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
    def get(self, request, pk):
        posting = get_object_or_404(Post, pk=pk)
        serializer_class = PostDetailSerializer(posting)
        return Response(serializer_class.data)

    def post(self, request, pk):
        posting = get_object_or_404(Post, pk=pk)
        serializer_class = PostPasswordSerializer(posting, data=request.data, partial=True)
        if serializer_class.is_valid():
            return HttpResponseRedirect(reverse("board:post", args=(pk, )))
        return Response("incorrect password", status=status.HTTP_403_FORBIDDEN)


class PostUpdateView(APIView):
    # def get(self, request, pk):
    #     posting = get_object_or_404(Post, pk=pk)
    #     serializer_class = PostDetailSerializer(posting)
    #     return Response(serializer_class.data)

    def put(self, request, pk):
        posting = get_object_or_404(Post, pk=pk)
        serializer_class = PostDetailSerializer(posting, data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        posting = get_object_or_404(Post, id=pk)
        serializer_class = PostDetailSerializer(posting, data=request.data, partial=True)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        posting = get_object_or_404(Post, pk=pk)
        posting.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
