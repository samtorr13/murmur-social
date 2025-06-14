from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from post.models import Post
from .serializer import PostSerializer

class PostListAPIView(APIView):
    def get(self, request):
        posts = Post.objects.all().order_by('-creat_date')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)