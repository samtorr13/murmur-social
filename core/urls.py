from django.urls import path
from .views import PostListAPIView, PostDetailAPIView, PostCreateAPIView, CommentAPIView, CommentPPostAPIView, \
    ReportCreateAPIView

urlpatterns = [
    path('posts/', PostListAPIView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailAPIView.as_view(), name='post-detail'),
    path('posts/create/', PostCreateAPIView.as_view(), name='post-create'),
    path('comments/', CommentAPIView.as_view(), name='comment-list'),
    path('comments/<int:post>/', CommentPPostAPIView.as_view(), name='comment-detail'),
    path('report/', ReportCreateAPIView.as_view(), name='report-create'),
]