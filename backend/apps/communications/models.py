import uuid
from django.db import models

class CorrespondenceStatus(models.TextChoices):
    SUBMITTED = 'SUBMITTED', 'Submitted'
    UNDER_REVIEW = 'UNDER_REVIEW', 'Under Review'
    REPLIED = 'REPLIED', 'Replied'
    CLOSED = 'CLOSED', 'Closed'

class Correspondence(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    correspondence_number = models.CharField(max_length=100, unique=True)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='correspondences')
    file = models.ForeignKey('files.GovernmentFile', on_delete=models.SET_NULL, null=True, blank=True, related_name='correspondences')
    sender = models.ForeignKey('accounts.User', on_delete=models.RESTRICT, related_name='sent_correspondences')
    recipient = models.ForeignKey('accounts.User', on_delete=models.RESTRICT, related_name='received_correspondences')
    subject = models.CharField(max_length=255)
    content = models.TextField()
    priority = models.CharField(max_length=20, default='MEDIUM')
    response_required = models.BooleanField(default=True)
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=30, choices=CorrespondenceStatus.choices, default=CorrespondenceStatus.SUBMITTED)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.correspondence_number} - {self.subject}"

class ProjectCommunication(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='communications')
    sender = models.ForeignKey('accounts.User', on_delete=models.RESTRICT)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    priority = models.CharField(max_length=20, default='NORMAL')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project.project_code} - {self.subject}"
