"""
Compliance views for application management and tracking.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Application, ComplianceScore, Remediation, Evidence
from .forms import ApplicationForm, RemediationForm


@login_required
def application_list(request):
    """List all applications."""
    if request.user.is_developer:
        applications = Application.objects.filter(owner=request.user)
    else:
        applications = Application.objects.all()
    
    return render(request, 'compliance/application_list.html', {
        'applications': applications
    })


@login_required
def application_detail(request, pk):
    """View application details with compliance history."""
    application = get_object_or_404(Application, pk=pk)
    
    if request.user.is_developer and application.owner != request.user:
        messages.error(request, 'Access denied.')
        return redirect('application_list')
    
    audits = application.audits.order_by('-created_at')[:10]
    scores = application.compliance_scores.order_by('-calculated_at')[:10]
    
    return render(request, 'compliance/application_detail.html', {
        'application': application,
        'audits': audits,
        'scores': scores,
    })


@login_required
def application_create(request):
    """Register a new application."""
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            if request.user.is_developer:
                application.owner = request.user
            application.save()
            messages.success(request, 'Application registered successfully.')
            return redirect('application_detail', pk=application.pk)
    else:
        form = ApplicationForm()
    
    return render(request, 'compliance/application_form.html', {
        'form': form, 
        'action': 'Register'
    })


@login_required
def application_edit(request, pk):
    """Edit application details."""
    application = get_object_or_404(Application, pk=pk)
    
    if request.user.is_developer and application.owner != request.user:
        messages.error(request, 'Access denied.')
        return redirect('application_list')
    
    if request.method == 'POST':
        form = ApplicationForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            messages.success(request, 'Application updated successfully.')
            return redirect('application_detail', pk=pk)
    else:
        form = ApplicationForm(instance=application)
    
    return render(request, 'compliance/application_form.html', {
        'form': form, 
        'action': 'Edit',
        'application': application
    })


@login_required
def remediation_list(request):
    """List all remediations."""
    if request.user.is_developer:
        remediations = Remediation.objects.filter(
            assigned_to=request.user
        ) | Remediation.objects.filter(
            audit_response__audit__application__owner=request.user
        )
    else:
        remediations = Remediation.objects.all()
    
    remediations = remediations.distinct().order_by('-created_at')
    
    return render(request, 'compliance/remediation_list.html', {
        'remediations': remediations
    })


@login_required
def remediation_detail(request, pk):
    """View and update remediation details."""
    remediation = get_object_or_404(Remediation, pk=pk)
    
    if request.method == 'POST':
        form = RemediationForm(request.POST, instance=remediation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Remediation updated successfully.')
            return redirect('remediation_detail', pk=pk)
    else:
        form = RemediationForm(instance=remediation)
    
    return render(request, 'compliance/remediation_detail.html', {
        'remediation': remediation,
        'form': form
    })
