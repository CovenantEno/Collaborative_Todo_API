from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Todo(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_todos')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Collaborator(models.Model):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name='collaborators')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_todos')
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invitations_sent')
    invited_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('todo', 'user')

    def __str__(self):
        return f"{self.user.username} collaborates on {self.todo.title}"
