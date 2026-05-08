from rest_framework import serializers

from apps.projects.models import Project

class ProjectSerializer(serializers.ModelSerializer):
    """Serializes project data for CRUD operations."""
    class Meta:
        model = Project
        fields = (
            'id',
            'name',
            'description',
            'owner',
            'members',
            'created_at',
            'updated_at',
        )
        read_only_fields=('created_at', 'updated_at')


class ProjectStatsSerializer(serializers.Serializer):
    """Serializes aggregated task statistics for a project."""
    total_tasks = serializers.IntegerField()
    todo = serializers.IntegerField()
    in_progress = serializers.IntegerField()
    done = serializers.IntegerField()
    high_priority = serializers.IntegerField()
    overdue = serializers.IntegerField()