"""
Custom User model for DP-COMPASS platform.
Supports role-based access for Auditors, Developers, and Administrators.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.core.models import TimeStampedModel


class User(AbstractUser):
    """Custom user model with DPDP-specific roles."""
    
    ROLE_CHOICES = [
        ('auditor', 'Compliance Auditor'),
        ('developer', 'Developer/Application Owner'),
        ('admin', 'Administrator'),
    ]
    
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES, 
        default='developer',
        help_text='User role determines access permissions'
    )
    organization = models.CharField(
        max_length=255, 
        blank=True,
        help_text='Organization or department name'
    )
    designation = models.CharField(
        max_length=100, 
        blank=True,
        help_text='Job title or designation'
    )
    phone = models.CharField(max_length=20, blank=True)
    is_verified = models.BooleanField(
        default=False,
        help_text='Verified by administrator'
    )

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"
    
    @property
    def is_auditor(self):
        return self.role == 'auditor'
    
    @property
    def is_developer(self):
        return self.role == 'developer'
    
    @property
    def is_admin_user(self):
        return self.role == 'admin'


class UserActivity(TimeStampedModel):
    """Track user activities for audit trail."""
    
    ACTION_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('audit_create', 'Created Audit'),
        ('audit_complete', 'Completed Audit'),
        ('report_generate', 'Generated Report'),
        ('app_register', 'Registered Application'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    details = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        db_table = 'user_activities'
        ordering = ['-created_at']
        verbose_name = 'User Activity'
        verbose_name_plural = 'User Activities'

    def __str__(self):
        return f"{self.user.username} - {self.get_action_display()}"
