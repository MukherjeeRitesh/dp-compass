from django.contrib import admin
from .models import AuditCategory, ChecklistItem, Audit, AuditResponse


@admin.register(AuditCategory)
class AuditCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'dpdp_section', 'order', 'checklist_count', 'is_active')
    list_filter = ('is_active', 'dpdp_section')
    search_fields = ('name', 'description')
    ordering = ('order', 'name')


@admin.register(ChecklistItem)
class ChecklistItemAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'category', 'severity', 'order', 'is_active')
    list_filter = ('category', 'severity', 'is_active')
    search_fields = ('code', 'title', 'description')
    ordering = ('category', 'order', 'code')


@admin.register(Audit)
class AuditAdmin(admin.ModelAdmin):
    list_display = ('title', 'application', 'auditor', 'status', 'scheduled_date', 'created_at')
    list_filter = ('status', 'scheduled_date', 'created_at')
    search_fields = ('title', 'application__name', 'auditor__username')
    date_hierarchy = 'created_at'
    raw_id_fields = ('application', 'auditor')


@admin.register(AuditResponse)
class AuditResponseAdmin(admin.ModelAdmin):
    list_display = ('audit', 'checklist_item', 'status', 'reviewed_by', 'reviewed_at')
    list_filter = ('status', 'reviewed_at')
    search_fields = ('audit__title', 'checklist_item__code', 'findings')
    raw_id_fields = ('audit', 'checklist_item', 'reviewed_by')
