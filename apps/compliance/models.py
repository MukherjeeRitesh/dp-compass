"""
Compliance models for application tracking and remediation.
"""
from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel


class Application(TimeStampedModel):
    """Registered applications/systems under DPDP compliance assessment."""
    
    TYPE_CHOICES = [
        ('web', 'Web Application'),
        ('mobile', 'Mobile Application'),
        ('api', 'API/Service'),
        ('database', 'Database'),
        ('infrastructure', 'Infrastructure'),
        ('other', 'Other'),
    ]
    
    ENVIRONMENT_CHOICES = [
        ('production', 'Production'),
        ('staging', 'Staging'),
        ('development', 'Development'),
        ('testing', 'Testing'),
    ]
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    application_type = models.CharField(
        max_length=20, 
        choices=TYPE_CHOICES, 
        default='web'
    )
    environment = models.CharField(
        max_length=20, 
        choices=ENVIRONMENT_CHOICES, 
        default='production'
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='owned_applications'
    )
    department = models.CharField(max_length=255, blank=True)
    url = models.URLField(blank=True, help_text='Application URL if applicable')
    version = models.CharField(max_length=50, blank=True)
    data_categories = models.TextField(
        blank=True,
        help_text='Types of personal data processed'
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'applications'
        ordering = ['name']
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'

    def __str__(self):
        return f"{self.name} ({self.get_application_type_display()})"
    
    @property
    def latest_audit(self):
        return self.audits.order_by('-created_at').first()
    
    @property
    def latest_score(self):
        return self.compliance_scores.order_by('-calculated_at').first()


class ComplianceScore(TimeStampedModel):
    """Calculated compliance scores for applications."""
    
    application = models.ForeignKey(
        Application, 
        on_delete=models.CASCADE, 
        related_name='compliance_scores'
    )
    audit = models.ForeignKey(
        'audits.Audit',
        on_delete=models.CASCADE,
        related_name='scores'
    )
    overall_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        help_text='Overall compliance percentage'
    )
    critical_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True,
        help_text='Compliance percentage for critical items'
    )
    major_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True,
        help_text='Compliance percentage for major items'
    )
    calculated_at = models.DateTimeField(auto_now_add=True)
    calculated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        db_table = 'compliance_scores'
        ordering = ['-calculated_at']
        verbose_name = 'Compliance Score'
        verbose_name_plural = 'Compliance Scores'

    def __str__(self):
        return f"{self.application.name}: {self.overall_score}%"


class Remediation(TimeStampedModel):
    """Remediation actions for non-compliant items."""
    
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('deferred', 'Deferred'),
        ('wont_fix', "Won't Fix"),
    ]
    
    PRIORITY_CHOICES = [
        ('critical', 'Critical'),
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]
    
    audit_response = models.ForeignKey(
        'audits.AuditResponse',
        on_delete=models.CASCADE,
        related_name='remediations'
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='open'
    )
    priority = models.CharField(
        max_length=20, 
        choices=PRIORITY_CHOICES, 
        default='medium'
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_remediations'
    )
    due_date = models.DateField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolution_notes = models.TextField(blank=True)

    class Meta:
        db_table = 'remediations'
        ordering = ['-created_at']
        verbose_name = 'Remediation'
        verbose_name_plural = 'Remediations'

    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"


class Evidence(TimeStampedModel):
    """Evidence attachments for compliance claims."""
    
    TYPE_CHOICES = [
        ('document', 'Document'),
        ('screenshot', 'Screenshot'),
        ('policy', 'Policy Document'),
        ('log', 'System Log'),
        ('certificate', 'Certificate'),
        ('other', 'Other'),
    ]
    
    audit_response = models.ForeignKey(
        'audits.AuditResponse',
        on_delete=models.CASCADE,
        related_name='evidence_files'
    )
    title = models.CharField(max_length=255)
    evidence_type = models.CharField(
        max_length=20, 
        choices=TYPE_CHOICES, 
        default='document'
    )
    file = models.FileField(upload_to='evidence/%Y/%m/')
    description = models.TextField(blank=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        db_table = 'evidence'
        ordering = ['-created_at']
        verbose_name = 'Evidence'
        verbose_name_plural = 'Evidence Files'

    def __str__(self):
        return f"{self.title} ({self.get_evidence_type_display()})"
