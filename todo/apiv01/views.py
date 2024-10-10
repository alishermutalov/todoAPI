from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import LoginSerializer, LogoutSerializer, RegisterSerializer, TaskSerializer
from .models import Task
from .filters import TaskFilter

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
    

class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
        return Response({"message":"Task created successfully!"})
    

class TaskListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = TaskSerializer
    queryset = Task.objects.all().order_by('-created_at')
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter
    
    
class TaskDetailView(generics.RetrieveAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated,]
    
    def get_object(self):
        task = super().get_object()
        if task.user != self.request.user:
            self.permission_denied(self.request)
        return task
    
    
class TaskUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    
    def get_object(self):
        task = super().get_object()
        if task.user != self.request.user:
            self.permission_denied(self.request)
        return task

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    
class TaskDeleteView(generics.DestroyAPIView):
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        task = super().get_object()
        if task.user != self.request.user:
            self.permission_denied(self.request)
        return task

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)