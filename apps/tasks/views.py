from rest_framework.generics import get_object_or_404
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from .filters import TaskFilter
from .models import Task, Comment
from .permissions import IsTaskProjectMember, IsCommentProjectMember
from .serializers import TaskSerializer, CommentSerializer


class TaskViewSet(ModelViewSet):
    """
    Provides CRUD operations for tasks only for project members.

    Supports filtering by status, priority, project and assignee,
    search by title, and ordering by creation date, due date and priority.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsTaskProjectMember]

    ordering = ['-created_at']
    filterset_class = TaskFilter
    search_fields = ['title']
    ordering_fields = ['created_at', 'due_date', 'priority']

    def get_queryset(self):
        return (Task.objects
                .filter(project__members=self.request.user)
                .select_related('project', 'assignee', 'created_by')
                .distinct())

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class CommentViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    """
    Lists and creates comments for a task only for project members.

    Comments are ordered by creation date (newest first).
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsCommentProjectMember]

    ordering = ['-created_at']
    ordering_fields = ['created_at']


    def get_queryset(self):
        task_id = self.kwargs.get('task_id')
        return (Comment.objects.filter(task_id=task_id,
                                       task__project__members=self.request.user)
                .select_related('task', 'author')
        )

    def perform_create(self, serializer):
        task = get_object_or_404(Task, pk=self.kwargs.get('task_id'))
        serializer.save(author=self.request.user, task=task)


