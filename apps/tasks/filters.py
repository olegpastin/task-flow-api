import django_filters

from apps.tasks.models import TaskStatus, TaskPriorities, Task


class TaskFilter(django_filters.FilterSet):
    """
    Provides filtering for tasks by status, priority, project and assignee,
    as well as by due date range.
    """
    due_date_from = django_filters.DateFilter(
        field_name='due_date',
        lookup_expr='gte',
    )
    due_date_to = django_filters.DateFilter(
        field_name='due_date',
        lookup_expr='lte',
    )

    status = django_filters.MultipleChoiceFilter(
        choices=TaskStatus.choices
    )

    priority = django_filters.MultipleChoiceFilter(
        choices=TaskPriorities.choices
    )

    class Meta:
        model = Task
        fields = (
            'status',
            'priority',
            'project',
            'assignee',
            'due_date_from',
            'due_date_to',
        )
