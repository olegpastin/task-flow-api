from rest_framework.routers import DefaultRouter
from django.urls import path

from apps.tasks.views import TaskViewSet, CommentViewSet

app_name = 'tasks'

router = DefaultRouter()
router.register(prefix='tasks', viewset=TaskViewSet)

urlpatterns = router.urls + [
    path('tasks/<int:task_id>/comments/',
         CommentViewSet.as_view({
             'get': 'list',
             'post': 'create',
         }), name='task-comments')
]
