"""
Core views for DP-COMPASS platform.
Dashboard and home page views.
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from apps.compliance.models import Application, ComplianceScore
from apps.audits.models import Audit, AuditResponse


def home(request):
    """Landing page / Home view."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'core/home.html')


@login_required
def dashboard(request):
    """Main dashboard with compliance overview."""
    user = request.user
    
    # Base querysets
    app_qs = Application.objects.all()
    audit_qs = Audit.objects.all()
    score_qs = ComplianceScore.objects.select_related('application')
    
    # Filter based on user role
    if user.is_auditor:
        app_qs = app_qs.filter(audits__auditor=user).distinct()
        audit_qs = audit_qs.filter(auditor=user)
        score_qs = score_qs.filter(application__audits__auditor=user).distinct()
    elif user.is_developer:
        app_qs = app_qs.filter(owner=user)
        audit_qs = audit_qs.filter(application__owner=user)
        score_qs = score_qs.filter(application__owner=user)
        
    context = {
        'total_applications': app_qs.count(),
        'pending_audits': audit_qs.filter(status='pending').count(),
        'completed_audits': audit_qs.filter(status='completed').count(),
        'in_progress_audits': audit_qs.filter(status='in_progress').count(),
        'recent_audits': audit_qs.order_by('-created_at')[:5],
        'compliance_scores': score_qs.order_by('-calculated_at')[:5],
    }
    
    return render(request, 'core/dashboard.html', context)
