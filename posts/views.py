from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models import Posting, Comment
from posts.serializers import PostingSimpleSerializer, PostingCreateSerializer


# Create your views here.

class PostingsView(APIView):
    def get(self, request):
        queryset = get_list_or_404(Posting)
        serializer_class = PostingSimpleSerializer(data=queryset, many=True)
        serializer_class.is_valid()
        return Response(serializer_class.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer_class = PostingCreateSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
