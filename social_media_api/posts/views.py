from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.filters import SearchFilter
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.contenttypes.models import ContentType
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from notifications.models import Notification


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for CRUD operations on Post model.
    Users can only edit or delete their own posts.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for CRUD operations on Comment model.
    Users can only edit or delete their own comments.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)
        # Create notification if commenting on someone else's post
        if comment.post.author != self.request.user:
            Notification.objects.create(
                recipient=comment.post.author,
                actor=self.request.user,
                verb="commented on your post",
                content_type=ContentType.objects.get_for_model(comment.post),
                object_id=comment.post.id
            )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def feed(request):
    """
    Generate a feed based on posts from users that the current user follows.
    Returns posts ordered by creation date, showing the most recent posts at the top.
    """
    followed_users = request.user.following.all()
    posts = Post.objects.filter(author__in=followed_users).order_by('-created_at')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request, pk):
    """Like a post"""
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    like, created = Like.objects.get_or_create(
        post=post,
        user=request.user
    )

    if not created:
        return Response({"message": "You already liked this post"}, status=status.HTTP_200_OK)

    # Create notification if liking someone else's post
    if post.author != request.user:
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb="liked your post",
            content_type=ContentType.objects.get_for_model(post),
            object_id=post.id
        )

    return Response({"message": "Post liked"}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unlike_post(request, pk):
    """Unlike a post"""
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    deleted_count, _ = Like.objects.filter(post=post, user=request.user).delete()

    if deleted_count == 0:
        return Response({"message": "You haven't liked this post"}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"message": "Post unliked"}, status=status.HTTP_200_OK)


