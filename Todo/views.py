from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import Todo, Collaborator
from .serializers import TodoSerializer, CollaboratorSerializer
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        owned = Todo.objects.filter(owner=user)
        shared = Todo.objects.filter(collaborators__user=user)
        return (owned | shared).distinct()

    def retrieve(self, request, *args, **kwargs):
        todo = self.get_object()
        if request.user != todo.owner and not todo.collaborators.filter(user=request.user).exists():
            return Response({'error': 'Access denied.'}, status=403)
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        todo = self.get_object()
        if request.user != todo.owner and not todo.collaborators.filter(user=request.user).exists():
            return Response({'error': 'Only owner or collaborators can update.'}, status=403)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        todo = self.get_object()
        if request.user != todo.owner:
            return Response({'error': 'Only owner can delete this todo.'}, status=403)
        return super().destroy(request, *args, **kwargs)

    # ---------------- Collaborator Endpoints ----------------
    @action(detail=True, methods=['post'], url_path='invite')
    def invite_collaborator(self, request, pk=None):
        todo = self.get_object()
        username = request.data.get('username')
        try:
            user_to_invite = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=404)

        if user_to_invite == request.user:
            return Response({'error': 'You cannot invite yourself.'}, status=400)

        collaborator, created = Collaborator.objects.get_or_create(
            todo=todo,
            user=user_to_invite,
            invited_by=request.user
        )

        if not created:
            return Response({'message': 'User already a collaborator.'}, status=200)

        serializer = CollaboratorSerializer(collaborator)
        return Response(serializer.data, status=201)

    @action(detail=True, methods=['post'], url_path='remove_collaborator')
    def remove_collaborator(self, request, pk=None):
        todo = self.get_object()
        if todo.owner != request.user:
            return Response({'error': 'Only the owner can remove collaborators.'}, status=403)

        username = request.data.get('username')
        if not username:
            return Response({'error': 'Username is required.'}, status=400)

        try:
            user_to_remove = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=404)

        try:
            collaborator = Collaborator.objects.get(todo=todo, user=user_to_remove)
            collaborator.delete()
            return Response({'message': f'{username} removed from collaborators.'}, status=200)
        except Collaborator.DoesNotExist:
            return Response({'error': 'User is not a collaborator.'}, status=404)

    @action(detail=True, methods=['get'], url_path='collaborators')
    def list_collaborators(self, request, pk=None):
        todo = self.get_object()
        collaborators = todo.collaborators.all()
        serializer = CollaboratorSerializer(collaborators, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='collaborators')
    def add_collaborator(self, request, pk=None):
        todo = self.get_object()
        if todo.owner != request.user:
            return Response({'error': 'Only owner can add collaborators.'}, status=403)

        username_or_email = request.data.get('username') or request.data.get('email')
        if not username_or_email:
            return Response({'error': 'Provide username or email.'}, status=400)

        try:
            if '@' in username_or_email:
                user_to_add = User.objects.get(email=username_or_email)
            else:
                user_to_add = User.objects.get(username=username_or_email)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=404)

        collaborator, created = Collaborator.objects.get_or_create(
            todo=todo,
            user=user_to_add,
            invited_by=request.user
        )

        if not created:
            return Response({'message': 'User already a collaborator.'}, status=200)

        serializer = CollaboratorSerializer(collaborator)
        return Response(serializer.data, status=201)

    @action(detail=True, methods=['delete'], url_path='collaborators/(?P<user_id>[^/.]+)')
    def delete_collaborator(self, request, pk=None, user_id=None):
        todo = self.get_object()
        if todo.owner != request.user:
            return Response({'error': 'Only owner can remove collaborators.'}, status=403)

        try:
            user_to_remove = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=404)

        try:
            collaborator = Collaborator.objects.get(todo=todo, user=user_to_remove)
            collaborator.delete()
            return Response({'message': f'{user_to_remove.username} removed from collaborators.'}, status=200)
        except Collaborator.DoesNotExist:
            return Response({'error': 'User is not a collaborator.'}, status=404)
