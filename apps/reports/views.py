"""
Report views for generating and viewing compliance reports.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from .models import ComplianceReport, ReportTemplate
from apps.audits.models import Audit


@login_required
def report_list(request):
    """List all compliance reports."""
    if request.user.is_auditor:
        reports = ComplianceReport.objects.filter(generated_by=request.user)
    elif request.user.is_developer:
        reports = ComplianceReport.objects.filter(
            audit__application__owner=request.user
        )
    else:
        reports = ComplianceReport.objects.all()
    
    return render(request, 'reports/report_list.html', {'reports': reports})


@login_required
def report_detail(request, pk):
    """View report details."""
    report = get_object_or_404(ComplianceReport, pk=pk)
    return render(request, 'reports/report_detail.html', {'report': report})


@login_required
def report_generate(request, audit_id):
    """Generate a new compliance report from an audit."""
    audit = get_object_or_404(Audit, pk=audit_id)
    
    if audit.status != 'completed':
        messages.error(request, 'Cannot generate report for incomplete audit.')
        return redirect('audit_detail', pk=audit_id)
    
    if request.method == 'POST':
        title = request.POST.get('title', f'Compliance Report - {audit.application.name}')
        
        # Calculate scores
        responses = audit.responses.all()
        total = responses.exclude(status='pending').count()
        compliant = responses.filter(status='compliant').count()
        non_compliant = responses.filter(status='non_compliant').count()
        
        compliance_score = round((compliant / total) * 100, 2) if total > 0 else 0
        
        # Create report
        report = ComplianceReport.objects.create(
            audit=audit,
            title=title,
            summary=f'Compliance assessment completed with score of {compliance_score}%',
            generated_by=request.user,
            generated_at=timezone.now(),
            status='generated'
        )
        
        messages.success(request, 'Report generated successfully.')
        return redirect('report_detail', pk=report.pk)
    
    templates = ReportTemplate.objects.filter(is_active=True)
    return render(request, 'reports/report_generate.html', {
        'audit': audit,
        'templates': templates
    })


@login_required
def report_export_pdf(request, pk):
    """Export report as PDF."""
    report = get_object_or_404(ComplianceReport, pk=pk)
    
    # Generate HTML content
    html_content = render_to_string('reports/report_pdf_template.html', {
        'report': report,
        'audit': report.audit,
        'responses': report.audit.responses.all(),
    })
    
    # For now, return HTML (PDF generation requires WeasyPrint setup)
    response = HttpResponse(html_content, content_type='text/html')
    response['Content-Disposition'] = f'attachment; filename="{report.title}.html"'
    return response


@login_required
def report_approve(request, pk):
    """Approve a compliance report (admin only)."""
    if not request.user.is_admin_user:
        messages.error(request, 'Only administrators can approve reports.')
        return redirect('report_detail', pk=pk)
    
    report = get_object_or_404(ComplianceReport, pk=pk)
    report.status = 'approved'
    report.approved_by = request.user
    report.approved_at = timezone.now()
    report.save()
    
    messages.success(request, 'Report approved successfully.')
    return redirect('report_detail', pk=pk)
