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
    
    # Get statistics based on user role
    context = {
        'total_applications': Application.objects.count(),
        'pending_audits': Audit.objects.filter(status='pending').count(),
        'completed_audits': Audit.objects.filter(status='completed').count(),
        'in_progress_audits': Audit.objects.filter(status='in_progress').count(),
    }
    
    # Get recent audits
    if user.role == 'auditor':
        context['recent_audits'] = Audit.objects.filter(auditor=user).order_by('-created_at')[:5]
    elif user.role == 'developer':
        context['recent_audits'] = Audit.objects.filter(
            application__owner=user
        ).order_by('-created_at')[:5]
    else:  # admin
        context['recent_audits'] = Audit.objects.all().order_by('-created_at')[:5]
    
    # Get compliance scores
    context['compliance_scores'] = ComplianceScore.objects.select_related(
        'application'
    ).order_by('-calculated_at')[:5]
    
    return render(request, 'core/dashboard.html', context)
