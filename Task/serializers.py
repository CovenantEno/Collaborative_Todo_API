from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task
from Todo.serializers import UserSerializer

class TaskSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'todo', 'title', 'description', 'completed', 'owner', 'created_at', 'updated_at']
        read_only_fields = ['owner', 'created_at', 'updated_at']
