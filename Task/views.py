# Task/views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.db import models

from .models import Task
from .serializers import TaskSerializer
from Todo.models import Todo

# --------------------------------
# Flat TaskViewSet
# --------------------------------
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(
            models.Q(todo__owner=user) |
            models.Q(todo__collaborators__user=user)
        ).distinct()

    def perform_create(self, serializer):
        todo_id = self.request.data.get('todo')
        todo = get_object_or_404(Todo, id=todo_id)
        if self.request.user != todo.owner and not todo.collaborators.filter(user=self.request.user).exists():
            raise PermissionError("You do not have permission to add a task to this todo.")
        serializer.save(owner=self.request.user, todo=todo)

    def update(self, request, *args, **kwargs):
        task = self.get_object()
        if request.user != task.todo.owner and not task.todo.collaborators.filter(user=request.user).exists():
            return Response({'error': 'Only owner or collaborators can update.'}, status=403)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        task = self.get_object()
        if request.user != task.todo.owner:
            return Response({'error': 'Only todo owner can delete this task.'}, status=403)
        return super().destroy(request, *args, **kwargs)


# --------------------------------
# Nested TaskViewSet
# --------------------------------
class NestedTaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        todo_id = self.kwargs["todo_pk"]
        todo = get_object_or_404(Todo, id=todo_id)
        user = self.request.user

        # Only owner or collaborator can see tasks
        if user != todo.owner and not todo.collaborators.filter(user=user).exists():
            return Task.objects.none()

        return Task.objects.filter(todo=todo)

    def perform_create(self, serializer):
        todo_id = self.kwargs["todo_pk"]
        todo = get_object_or_404(Todo, id=todo_id)
        user = self.request.user

        if user != todo.owner and not todo.collaborators.filter(user=user).exists():
            return Response({"error": "You cannot add tasks here"}, status=403)

        serializer.save(todo=todo, owner=user)
