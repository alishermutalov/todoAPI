from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    TASK_STATUS = (
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("complated", "Complated"),
    )
    
    title = models.CharField(max_length=255, verbose_name="Task title")
    description = models.TextField(null=True, blank=True, verbose_name="Description")
    status = models.CharField(max_length=15, choices=TASK_STATUS, default="pending")
    due_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.title} - {self.status}"

