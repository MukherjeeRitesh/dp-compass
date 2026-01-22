from django.contrib import admin
from .models import Application, ComplianceScore, Remediation, Evidence


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'application_type', 'environment', 'owner', 'department', 'is_active')
    list_filter = ('application_type', 'environment', 'is_active')
    search_fields = ('name', 'description', 'department')
    raw_id_fields = ('owner',)


@admin.register(ComplianceScore)
class ComplianceScoreAdmin(admin.ModelAdmin):
    list_display = ('application', 'audit', 'overall_score', 'critical_score', 'calculated_at')
    list_filter = ('calculated_at',)
    search_fields = ('application__name',)
    raw_id_fields = ('application', 'audit', 'calculated_by')


@admin.register(Remediation)
class RemediationAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'priority', 'assigned_to', 'due_date', 'created_at')
    list_filter = ('status', 'priority', 'due_date')
    search_fields = ('title', 'description')
    raw_id_fields = ('audit_response', 'assigned_to')


@admin.register(Evidence)
class EvidenceAdmin(admin.ModelAdmin):
    list_display = ('title', 'evidence_type', 'audit_response', 'uploaded_by', 'created_at')
    list_filter = ('evidence_type', 'created_at')
    search_fields = ('title', 'description')
    raw_id_fields = ('audit_response', 'uploaded_by')
