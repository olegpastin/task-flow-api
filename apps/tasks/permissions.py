from rest_framework.permissions import BasePermission

from apps.tasks.models import Task


class IsTaskProjectMember(BasePermission):
    """Allow access only to users who are members of the task's project."""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.project.members.filter(pk=request.user.pk).exists()


class IsCommentProjectMember(BasePermission):
    """Allow access only to users who are members of the comment's task project."""
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        if view.action == 'create':
            task_id = view.kwargs.get('task_id', False)
            return Task.objects.filter(
                pk=task_id,
                project__members=request.user
            ).exists()
        return True

    def has_object_permission(self, request, view, obj):
        return obj.task.project.members.filter(pk=request.user.pk).exists()