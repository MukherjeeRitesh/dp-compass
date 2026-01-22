from django.contrib import admin
from .models import ReportTemplate, ComplianceReport


@admin.register(ReportTemplate)
class ReportTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_default', 'is_active', 'created_at')
    list_filter = ('is_active', 'is_default')
    search_fields = ('name', 'description')


@admin.register(ComplianceReport)
class ComplianceReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'audit', 'status', 'generated_by', 'generated_at', 'approved_by')
    list_filter = ('status', 'generated_at', 'approved_at')
    search_fields = ('title', 'audit__application__name')
    raw_id_fields = ('audit', 'template', 'generated_by', 'approved_by')
