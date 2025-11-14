from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Todo, Collaborator
from Users.serializers import UserSerializer

class CollaboratorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Collaborator
        fields = ['id', 'user', 'invited_by', 'invited_at']
        read_only_fields = ['invited_by', 'invited_at']


class TodoSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    collaborators = CollaboratorSerializer(many=True, read_only=True)

    class Meta:
        model = Todo
        fields = ['id', 'owner', 'title', 'description', 'due_date', 'completed', 'collaborators', 'created_at']
        read_only_fields = ['owner', 'created_at']
