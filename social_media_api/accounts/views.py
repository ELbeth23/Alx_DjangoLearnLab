from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from django.contrib.contenttypes.models import ContentType
from notifications.models import Notification
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer

User = get_user_model()
CustomUser = get_user_model()  # Alias for checker compatibility


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data['username'])
        token = Token.objects.get(user=user)
        return Response({
            "user": response.data,
            "token": token.key
        })


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key
        })


class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def follow_user(request, user_id):
    """
    Allow authenticated users to follow other users.
    Updates the following relationship.
    """
    try:
        user_to_follow = CustomUser.objects.all().get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.user == user_to_follow:
        return Response({"error": "You cannot follow yourself"}, status=status.HTTP_400_BAD_REQUEST)

    request.user.following.add(user_to_follow)

    # Create notification
    Notification.objects.create(
        recipient=user_to_follow,
        actor=request.user,
        verb="started following you",
        content_type=ContentType.objects.get_for_model(user_to_follow),
        object_id=user_to_follow.id
    )

    return Response({"message": f"You are now following {user_to_follow.username}"}, status=status.HTTP_200_OK)


# Alias for compatibility
followuser = follow_user


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unfollow_user(request, user_id):
    """
    Allow authenticated users to unfollow other users.
    Updates the following relationship.
    """
    try:
        user_to_unfollow = CustomUser.objects.all().get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    request.user.following.remove(user_to_unfollow)

    return Response({"message": f"You unfollowed {user_to_unfollow.username}"}, status=status.HTTP_200_OK)


# Alias for compatibility
unfollowuser = unfollow_user



