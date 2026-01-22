"""
Report models for compliance report generation.
"""
from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel


class ReportTemplate(TimeStampedModel):
    """Standardized report templates."""
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    template_content = models.TextField(
        help_text='HTML template content for report generation'
    )
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'report_templates'
        verbose_name = 'Report Template'
        verbose_name_plural = 'Report Templates'

    def __str__(self):
        return self.name


class ComplianceReport(TimeStampedModel):
    """Generated compliance reports."""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('generated', 'Generated'),
        ('approved', 'Approved'),
        ('archived', 'Archived'),
    ]
    
    audit = models.ForeignKey(
        'audits.Audit',
        on_delete=models.CASCADE,
        related_name='reports'
    )
    template = models.ForeignKey(
        ReportTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    title = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='draft'
    )
    summary = models.TextField(blank=True)
    recommendations = models.TextField(blank=True)
    generated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='generated_reports'
    )
    generated_at = models.DateTimeField(null=True, blank=True)
    pdf_file = models.FileField(
        upload_to='reports/%Y/%m/', 
        blank=True, 
        null=True
    )
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_reports'
    )
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'compliance_reports'
        ordering = ['-created_at']
        verbose_name = 'Compliance Report'
        verbose_name_plural = 'Compliance Reports'

    def __str__(self):
        return f"{self.title} - {self.audit.application.name}"
