from rest_framework.permissions import BasePermission

from apps.projects.models import Project


class IsOwnerOrMember(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if Project.objects.filter(
            members=request.user,
            pk=obj.pk
        ).exists():
            return True

        return obj.owner == request.user


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user