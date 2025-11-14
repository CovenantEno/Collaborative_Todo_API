# Task/urls.py

from django.urls import path, include
from rest_framework_nested import routers
from Todo.views import TodoViewSet
from .views import TaskViewSet, NestedTaskViewSet

# Main router
router = routers.DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='tasks')
router.register(r'todos', TodoViewSet, basename='todos')

# Nested router: /api/todos/<todo_pk>/tasks/
todos_router = routers.NestedDefaultRouter(router, r'todos', lookup='todo')
todos_router.register(r'tasks', NestedTaskViewSet, basename='todo-tasks')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(todos_router.urls)),
]
