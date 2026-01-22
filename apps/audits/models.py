"""
Audit models for DPDP compliance assessment.
Includes checklist categories, items, and audit responses.
"""
from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel, DPDPSection


class AuditCategory(TimeStampedModel):
    """Categories for DPDP compliance audit checklist."""
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    dpdp_section = models.ForeignKey(
        DPDPSection, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='categories'
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'audit_categories'
        ordering = ['order', 'name']
        verbose_name = 'Audit Category'
        verbose_name_plural = 'Audit Categories'

    def __str__(self):
        return self.name
    
    @property
    def checklist_count(self):
        return self.checklist_items.filter(is_active=True).count()


class ChecklistItem(TimeStampedModel):
    """Individual compliance checklist items."""
    
    SEVERITY_CHOICES = [
        ('critical', 'Critical'),
        ('major', 'Major'),
        ('minor', 'Minor'),
        ('advisory', 'Advisory'),
    ]
    
    category = models.ForeignKey(
        AuditCategory, 
        on_delete=models.CASCADE, 
        related_name='checklist_items'
    )
    code = models.CharField(
        max_length=20, 
        unique=True,
        help_text='Unique identifier for the checklist item (e.g., DC-001)'
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    guidance = models.TextField(
        blank=True,
        help_text='Guidance for auditors on how to evaluate this item'
    )
    evidence_required = models.TextField(
        blank=True,
        help_text='Types of evidence required for compliance'
    )
    severity = models.CharField(
        max_length=20, 
        choices=SEVERITY_CHOICES, 
        default='major'
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'checklist_items'
        ordering = ['category', 'order', 'code']
        verbose_name = 'Checklist Item'
        verbose_name_plural = 'Checklist Items'

    def __str__(self):
        return f"{self.code}: {self.title}"


class Audit(TimeStampedModel):
    """Audit session for an application/system."""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
    ]
    
    application = models.ForeignKey(
        'compliance.Application',
        on_delete=models.CASCADE,
        related_name='audits'
    )
    auditor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='conducted_audits'
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    scheduled_date = models.DateField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'audits'
        ordering = ['-created_at']
        verbose_name = 'Audit'
        verbose_name_plural = 'Audits'

    def __str__(self):
        return f"{self.title} - {self.application.name}"
    
    @property
    def progress_percentage(self):
        total = self.responses.count()
        if total == 0:
            return 0
        completed = self.responses.exclude(status='pending').count()
        return int((completed / total) * 100)
    
    @property
    def compliance_score(self):
        """Calculate compliance score based on responses."""
        responses = self.responses.exclude(status='pending')
        if not responses.exists():
            return None
        
        compliant = responses.filter(status='compliant').count()
        total = responses.count()
        return round((compliant / total) * 100, 2)


class AuditResponse(TimeStampedModel):
    """Responses to checklist items during an audit."""
    
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('compliant', 'Compliant'),
        ('non_compliant', 'Non-Compliant'),
        ('partially_compliant', 'Partially Compliant'),
        ('not_applicable', 'Not Applicable'),
    ]
    
    audit = models.ForeignKey(
        Audit, 
        on_delete=models.CASCADE, 
        related_name='responses'
    )
    checklist_item = models.ForeignKey(
        ChecklistItem, 
        on_delete=models.CASCADE,
        related_name='responses'
    )
    status = models.CharField(
        max_length=25, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    findings = models.TextField(
        blank=True,
        help_text='Detailed findings from the audit'
    )
    evidence_notes = models.TextField(
        blank=True,
        help_text='Notes about evidence reviewed'
    )
    recommendations = models.TextField(
        blank=True,
        help_text='Recommendations for improvement'
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_responses'
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'audit_responses'
        ordering = ['checklist_item__category', 'checklist_item__order']
        unique_together = ['audit', 'checklist_item']
        verbose_name = 'Audit Response'
        verbose_name_plural = 'Audit Responses'

    def __str__(self):
        return f"{self.audit.title} - {self.checklist_item.code}: {self.get_status_display()}"
