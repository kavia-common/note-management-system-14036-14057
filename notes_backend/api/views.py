from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .models import Note
from .serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    NoteSerializer,
)

# PUBLIC_INTERFACE
@api_view(['GET'])
@permission_classes([AllowAny])
def health(request):
    """Health check endpoint."""
    return Response({"message": "Server is up!"})


# PUBLIC_INTERFACE
class RegisterView(generics.CreateAPIView):
    """
    User registration endpoint.
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer

# PUBLIC_INTERFACE
class LoginView(APIView):
    """
    User login endpoint. Returns token on successful login.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({"error": "Invalid username or password."}, status=status.HTTP_401_UNAUTHORIZED)
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.id, "username": user.username})

# PUBLIC_INTERFACE
class LogoutView(APIView):
    """
    User logout endpoint; deletes token and logs out.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.auth.delete()  # Delete the token
        logout(request)
        return Response({"message": "Logged out successfully."})

# PUBLIC_INTERFACE
class UserInfoView(APIView):
    """
    Returns authenticated user's information.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
        })

# PUBLIC_INTERFACE
class NoteViewSet(viewsets.ModelViewSet):
    """
    CRUD ViewSet for Note operations. Requires authentication.
    """
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
