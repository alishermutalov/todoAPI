from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import LoginView, LogoutView, RegisterView, TaskCreateView,\
    TaskListView, TaskDetailView, TaskUpdateView, TaskDeleteView,\
        CommentCreateView, CommentListView

urlpatterns = [
    #Auth
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    #Task
    path('tasks/', TaskListView.as_view(), name="task-list"),
    path('task/create/', TaskCreateView.as_view(), name="create-task"),
    path('task/detail/<int:pk>/', TaskDetailView.as_view(), name="task-detail"),
    path('task/update/<int:pk>/', TaskUpdateView.as_view(), name="task-update"),
    path('task/delete/<int:pk>/', TaskDeleteView.as_view(), name="task-delete"),
    #Comment
    path('tasks/<int:task_id>/comments/', CommentListView.as_view(), name='comment-list'),
    path('tasks/<int:task_id>/comments/create/', CommentCreateView.as_view(), name='comment-create'),
]
