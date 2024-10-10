from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.utils import extend_schema
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import LoginSerializer, LogoutSerializer, \
    RegisterSerializer, TaskSerializer, CommentSerializer
from .models import Task, Comment
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


@extend_schema(
    summary="Refresh JWT token",
    request=None,
    responses={
        200: 'Token refreshed successfully!',
        400: 'Bad Request',
    },
    description="Use this endpoint to refresh your JWT token when it expires."
)
class CustomTokenRefreshView(TokenRefreshView):
    pass


@extend_schema(
    summary="Logout user",
    request=LogoutSerializer,
    responses={
        200: 'Successfully logged out!',
        400: 'Token not found or invalid',
    },
    description="Logs out the user by blacklisting the refresh token."
)
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
    

@extend_schema(
    summary="Create a new task",
    request=TaskSerializer,
    responses={
        201: 'Task created successfully!',
        400: 'Bad Request',
    },
    description="Create a new task. Users can assign a title, description, due date, and status."
)
class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
        return Response({"message":"Task created successfully!"})
    

@extend_schema(
    summary="Get list of tasks",
    responses={
        200: 'OK',
        401: 'Unauthorized',
    },
    description="Fetch a list of all tasks associated with the authenticated user, ordered by creation date."
)
class TaskListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = TaskSerializer
    queryset = Task.objects.all().order_by('-created_at')
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter
    

@extend_schema(
    summary="Retrieve task details",
    responses={
        200: 'OK',
        403: 'Permission denied',
        404: 'Task not found',
    },
    description="Fetch details of a specific task owned by the authenticated user."
)   
class TaskDetailView(generics.RetrieveAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated,]
    
    def get_object(self):
        task = super().get_object()
        if task.user != self.request.user:
            self.permission_denied(self.request)
        return task
    

@extend_schema(
    summary="Update a task",
    request=TaskSerializer,
    responses={
        200: 'OK',
        400: 'Bad Request',
        403: 'Permission denied',
        404: 'Task not found',
    },
    description="Update an existing task. The user must own the task to modify it."
)
class TaskUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    
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
    

@extend_schema(
    summary="Delete a task",
    responses={
        204: 'No Content',
        403: 'Permission denied',
        404: 'Task not found',
    },
    description="Delete a task. The user must own the task to delete it."
)    
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
    

@extend_schema(
    summary="Create a new comment for a task",
    request=CommentSerializer,
    responses={
        201: 'Comment created successfully!',
        400: 'Bad Request',
        403: 'Permission denied',
        404: 'Task not found',
    },
    description="Create a new comment for a specific task. The user must be authenticated."
)    
class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]  

    def perform_create(self, serializer):
        task_id = self.kwargs.get('task_id')  
        serializer.save(task_id=task_id, user=self.request.user) 
    

@extend_schema(
    summary="Get comments for a task",
    responses={
        200: 'OK',
        403: 'Permission denied',
        404: 'Task not found',
    },
    description="Fetch all comments for a specific task."
)    
class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated] 
    
    def get_queryset(self):
        task_id = self.kwargs.get('task_id')
        return Comment.objects.filter(task_id=task_id).order_by('-created_at')