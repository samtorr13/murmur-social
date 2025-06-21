from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework import status, permissions
from comments.models import Comment
from post.models import Post

from .serializer import PostSerializer, PostCreateSerializer, CommentSerializer, ReportSerializer

class PostListAPIView(APIView):
    def get(self, request):
        posts = Post.objects.all().order_by('-creat_date')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticated]

class CommentAPIView(APIView):
    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentPPostAPIView(ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post = self.kwargs['post']
        return Comment.objects.filter(post=post)

class ReportCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Solo usuarios logueados pueden reportar

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['reporter'] = request.user.id  # Inyectamos el usuario autenticado como reportero

        serializer = ReportSerializer(data=data)
        if serializer.is_valid():
            report = serializer.save()
            return Response(ReportSerializer(report).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
