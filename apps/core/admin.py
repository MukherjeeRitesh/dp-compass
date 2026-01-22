from django.contrib import admin
from .models import DPDPSection


@admin.register(DPDPSection)
class DPDPSectionAdmin(admin.ModelAdmin):
    list_display = ('section_number', 'title', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('section_number', 'title', 'description')
