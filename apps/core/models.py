"""
Core models for DP-COMPASS platform.
Base models providing common functionality across all apps.
"""
from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    """Abstract base model with created and modified timestamps."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class DPDPSection(models.Model):
    """DPDP Act Sections for reference in compliance tracking."""
    section_number = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'dpdp_sections'
        ordering = ['section_number']
        verbose_name = 'DPDP Section'
        verbose_name_plural = 'DPDP Sections'

    def __str__(self):
        return f"Section {self.section_number}: {self.title}"
