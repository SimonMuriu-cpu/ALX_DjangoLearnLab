# api/views_auth.py

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer

# -----------------------------
# User Registration
# -----------------------------
class UserRegistrationView(generics.CreateAPIView):
    """
    Endpoint for user registration.
    POST request with username, password, email (optional) creates a new user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


# -----------------------------
# User Login
# -----------------------------
class UserLoginView(APIView):
    """
    Endpoint for user login.
    Returns an authentication token if username & password are correct.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        username = request.data.get("username")
        password = request.data.get("password")

        if username is None or password is None:
            return Response(
                {"error": "Please provide both username and password."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(username=username, password=password)
        if not user:
            return Response(
                {"error": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)


# -----------------------------
# User Logout
# -----------------------------
class UserLogoutView(APIView):
    """
    Endpoint for user logout.
    Deletes the token so it cannot be used again.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        user = request.user
        # Delete the token to logout
        Token.objects.filter(user=user).delete()
        return Response(
            {"success": "Logged out successfully."}, status=status.HTTP_200_OK
        )


# -----------------------------
# User Profile
# -----------------------------
class UserProfileView(generics.RetrieveAPIView):
    """
    Endpoint to get the authenticated user's profile.
    Requires authentication.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
