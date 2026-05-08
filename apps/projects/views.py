from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q, Count
from django.utils import timezone

from .models import Project
from .permissions import IsOwnerOrMember, IsOwner
from .serializers import ProjectSerializer, ProjectStatsSerializer
from ..tasks.models import Task, TaskStatus, TaskPriorities


class ProjectViewSet(ModelViewSet):
    """
    Provides CRUD operations for projects.

    Users can only access projects where they are members.
    Any authenticated user can create a project.
    Only owner can delete or update project.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(members=self.request.user).distinct()

    def perform_create(self, serializer):
        project = serializer.save(owner=self.request.user)
        project.members.add(self.request.user)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsOwnerOrMember()]
        if self.action == 'create':
            return [IsAuthenticated()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwner()]

    @extend_schema(
        summary='Get project statistics',
        description='Returns task statistics for a project available to the current user.',
        responses=ProjectStatsSerializer,
    )
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Return aggregated task statistics for a project."""
        project = self.get_object()
        data = Task.objects.filter(project=project).aggregate(
            total_tasks=Count('pk'),
            todo=Count('pk', filter=Q(status=TaskStatus.TODO)),
            in_progress=Count('pk', filter=Q(status=TaskStatus.IN_PROGRESS)),
            done=Count('pk', filter=Q(status=TaskStatus.DONE)),
            high_priority=Count('pk', filter=Q(priority=TaskPriorities.HIGH)),
            overdue=Count(
                'pk',
                filter=Q(due_date__lt=timezone.now()) & ~Q(status=TaskStatus.DONE),
            ),
        )
        serializer = ProjectStatsSerializer(instance=data)

        return Response(data=serializer.data, status=status.HTTP_200_OK)