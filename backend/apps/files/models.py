import uuid
from django.db import models

class FilePriority(models.TextChoices):
    LOW = 'LOW', 'Low'
    MEDIUM = 'MEDIUM', 'Medium'
    HIGH = 'HIGH', 'High'
    URGENT = 'URGENT', 'Urgent / Immediate'

class FileConfidentiality(models.TextChoices):
    PUBLIC = 'PUBLIC', 'Public'
    INTERNAL = 'INTERNAL', 'Internal'
    CONFIDENTIAL = 'CONFIDENTIAL', 'Confidential'
    RESTRICTED = 'RESTRICTED', 'Restricted'

class FileStatus(models.TextChoices):
    DRAFT = 'DRAFT', 'Draft'
    REGISTERED = 'REGISTERED', 'Registered / Diarized'
    ASSIGNED = 'ASSIGNED', 'Assigned'
    UNDER_PROCESS = 'UNDER_PROCESS', 'Under Process'
    PENDING_ACTION = 'PENDING_ACTION', 'Pending Action'
    RETURNED = 'RETURNED', 'Returned for Clarification'
    FORWARDED = 'FORWARDED', 'Forwarded'
    UNDER_CONSULTATION = 'UNDER_CONSULTATION', 'Under Parallel Consultation'
    RECOMMENDED = 'RECOMMENDED', 'Recommended'
    PENDING_APPROVAL = 'PENDING_APPROVAL', 'Pending Competent Authority Approval'
    APPROVED = 'APPROVED', 'Approved'
    REJECTED = 'REJECTED', 'Rejected'
    COMPLETED = 'COMPLETED', 'Completed'
    CLOSED = 'CLOSED', 'Closed'
    ARCHIVED = 'ARCHIVED', 'Archived'

class RecommendationChoices(models.TextChoices):
    RECOMMEND_APPROVAL = 'RECOMMEND_APPROVAL', 'Recommend Approval'
    RECOMMEND_REJECTION = 'RECOMMEND_REJECTION', 'Recommend Rejection'
    RECOMMEND_MODIFICATION = 'RECOMMEND_MODIFICATION', 'Recommend Modification'
    NEUTRAL = 'NEUTRAL', 'For Information / Examination'

class DecisionTypeChoices(models.TextChoices):
    APPROVED = 'APPROVED', 'Approved'
    REJECTED = 'REJECTED', 'Rejected'
    APPROVED_WITH_CONDITIONS = 'APPROVED_WITH_CONDITIONS', 'Approved with Conditions'
    RETURNED = 'RETURNED', 'Returned for Clarification'

class GovernmentFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file_number = models.CharField(max_length=100, unique=True)
    subject = models.CharField(max_length=255)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='government_files')
    department = models.ForeignKey('organizations.Department', on_delete=models.SET_NULL, null=True, blank=True)
    office = models.ForeignKey('organizations.Office', on_delete=models.SET_NULL, null=True, blank=True)
    file_type = models.CharField(max_length=100, default='GENERAL')
    priority = models.CharField(max_length=20, choices=FilePriority.choices, default=FilePriority.MEDIUM)
    confidentiality = models.CharField(max_length=20, choices=FileConfidentiality.choices, default=FileConfidentiality.INTERNAL)
    
    originator = models.ForeignKey('accounts.User', on_delete=models.RESTRICT, related_name='originated_files')
    current_holder = models.ForeignKey('accounts.User', on_delete=models.RESTRICT, related_name='held_files')
    current_department = models.ForeignKey('organizations.Department', on_delete=models.SET_NULL, null=True, blank=True, related_name='held_dept_files')
    
    status = models.CharField(max_length=30, choices=FileStatus.choices, default=FileStatus.REGISTERED)
    due_date = models.DateTimeField(null=True, blank=True)
    
    is_overdue = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.file_number} - {self.subject}"

class FileNote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.ForeignKey(GovernmentFile, on_delete=models.CASCADE, related_name='notes')
    note_number = models.IntegerField()
    author = models.ForeignKey('accounts.User', on_delete=models.RESTRICT, related_name='authored_notes')
    content = models.TextField()
    recommendation = models.CharField(max_length=30, choices=RecommendationChoices.choices, default=RecommendationChoices.NEUTRAL)
    is_finalized = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['note_number']
        unique_together = ('file', 'note_number')

    def __str__(self):
        return f"{self.file.file_number} - Note #{self.note_number} by {self.author.username}"

class FileMovement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.ForeignKey(GovernmentFile, on_delete=models.CASCADE, related_name='movements')
    from_user = models.ForeignKey('accounts.User', on_delete=models.RESTRICT, related_name='sent_movements')
    to_user = models.ForeignKey('accounts.User', on_delete=models.RESTRICT, related_name='received_movements')
    from_department = models.ForeignKey('organizations.Department', on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_dept_movements')
    to_department = models.ForeignKey('organizations.Department', on_delete=models.SET_NULL, null=True, blank=True, related_name='received_dept_movements')
    action = models.CharField(max_length=100)
    remarks = models.TextField(blank=True, default='')
    expected_action = models.CharField(max_length=150, blank=True, default='')
    due_date = models.DateTimeField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.file.file_number}: {self.from_user.username} -> {self.to_user.username} ({self.action})"

class FileParticipant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.ForeignKey(GovernmentFile, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    role_in_file = models.CharField(max_length=50)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('file', 'user')

class FileDecision(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.ForeignKey(GovernmentFile, on_delete=models.CASCADE, related_name='decisions')
    decision_type = models.CharField(max_length=30, choices=DecisionTypeChoices.choices)
    decision_by = models.ForeignKey('accounts.User', on_delete=models.RESTRICT)
    remarks = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.file_number} - {self.decision_type} by {self.decision_by.username}"
