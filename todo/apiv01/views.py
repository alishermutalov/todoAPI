from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import LoginSerializer, LogoutSerializer, RegisterSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(
    summary="Register a new user",
    request=RegisterSerializer,
    responses={
        201: 'User registered successfully!',
        400: 'Bad Request',
    },
    description=(
        "Register a new user. \n\n"
        "Example:\n"
        "- Username: `test_user`\n"
        "\n"
        "- Password: `test_password`\n"
        "You can use this test user for testing the API."
    ),
)
class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message":"User registered successfully!",
                "data":serializer.data
                }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            data={
                "message":"Successfully Logged out!"
                },
            status=status.HTTP_200_OK)


@extend_schema(
    summary="Login user",
    request=LoginSerializer,
    responses={
        200: 'User logged in successfully!',
        400: 'Bad Request',
    },
    description=(
        "Login test user. \n\n"
        "Test user info:\n"
        "- Username: `new_user`\n"
        "\n"
        "- Password: `new_password123`\n"
        "You can use this test user for testing the API."
    ),
)
class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    
