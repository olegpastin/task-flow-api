from rest_framework import serializers

from apps.tasks.models import Task, Comment


class TaskSerializer(serializers.ModelSerializer):
    """Serializes task data and validates project membership and assignment."""
    class Meta:
        model = Task
        fields = (
            'id',
            'project',
            'title',
            'description',
            'status',
            'priority',
            'assignee',
            'created_by',
            'due_date',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('created_by', 'created_at', 'updated_at')

    def validate(self, attrs):
        project = attrs.get('project') or getattr(self.instance, 'project', None)
        assignee = attrs.get('assignee')
        if assignee is None:
            assignee = getattr(self.instance, 'assignee', None)
        request = self.context.get('request')

        if request and request.user and project and not project.members.filter(pk=request.user.pk).exists():
            raise serializers.ValidationError(
                {'project': 'You are not a member of this project.'}
            )

        if project and assignee and not project.members.filter(pk=assignee.pk).exists():
            raise serializers.ValidationError(
                {'assignee': 'This user is not a project member.'}
            )

        return attrs


class CommentSerializer(serializers.ModelSerializer):
    """Serializes comments with automatic author assignment."""
    author = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:
        model = Comment
        fields = (
            'id',
            'task',
            'author',
            'text',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('author', 'created_at', 'updated_at')
