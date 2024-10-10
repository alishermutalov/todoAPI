import django_filters
from .models import Task

class TaskFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Task.TASK_STATUS)
    due_date = django_filters.DateTimeFilter()

    class Meta:
        model = Task
        fields = ['status', 'due_date']
