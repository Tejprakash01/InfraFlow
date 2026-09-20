import uuid
from django.db import models

class TaskStatus(models.TextChoices):
    OPEN = 'OPEN', 'Open'
    IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
    COMPLETED = 'COMPLETED', 'Completed'

class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='tasks')
    file = models.ForeignKey('files.GovernmentFile', on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    assigned_to = models.ForeignKey('accounts.User', on_delete=models.RESTRICT, related_name='assigned_tasks')
    assigned_by = models.ForeignKey('accounts.User', on_delete=models.RESTRICT, related_name='created_tasks')
    status = models.CharField(max_length=20, choices=TaskStatus.choices, default=TaskStatus.OPEN)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.status})"
