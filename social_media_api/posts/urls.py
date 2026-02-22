from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, feed_view, LikePostView, UnlikePostView
from django.urls import path

router = DefaultRouter()
router.register('posts', PostViewSet, basename='post')
router.register('comments', CommentViewSet, basename='comment')

urlpatterns = router.urls + [
    path('feed/', feed_view, name='feed'),
    path('posts/<int:pk>/like/', LikePostView.as_view(), name='like-post'),
    path('posts/<int:pk>/unlike/', UnlikePostView.as_view(), name='unlike-post'),
]