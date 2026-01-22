"""
Audit views for managing compliance audits.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from .models import AuditCategory, ChecklistItem, Audit, AuditResponse
from .forms import AuditForm, AuditResponseForm


@login_required
def audit_list(request):
    """List all audits based on user role."""
    user = request.user
    
    if user.is_auditor:
        audits = Audit.objects.filter(auditor=user)
    elif user.is_developer:
        audits = Audit.objects.filter(application__owner=user)
    else:  # admin
        audits = Audit.objects.all()
    
    return render(request, 'audits/audit_list.html', {'audits': audits})


@login_required
def audit_detail(request, pk):
    """View audit details and responses."""
    audit = get_object_or_404(Audit, pk=pk)
    
    # Check permissions
    if not (request.user.is_admin_user or 
            request.user == audit.auditor or 
            request.user == audit.application.owner):
        messages.error(request, 'Access denied.')
        return redirect('audit_list')
    
    responses = audit.responses.select_related('checklist_item', 'checklist_item__category')
    categories = AuditCategory.objects.filter(
        checklist_items__responses__audit=audit
    ).distinct()
    
    return render(request, 'audits/audit_detail.html', {
        'audit': audit,
        'responses': responses,
        'categories': categories,
    })


@login_required
def audit_create(request):
    """Create a new audit."""
    if not request.user.is_auditor and not request.user.is_admin_user:
        messages.error(request, 'Only auditors can create audits.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AuditForm(request.POST)
        if form.is_valid():
            audit = form.save(commit=False)
            audit.auditor = request.user
            audit.save()
            
            # Create audit responses for all active checklist items
            checklist_items = ChecklistItem.objects.filter(is_active=True)
            for item in checklist_items:
                AuditResponse.objects.create(audit=audit, checklist_item=item)
            
            messages.success(request, 'Audit created successfully.')
            return redirect('audit_detail', pk=audit.pk)
    else:
        form = AuditForm()
    
    return render(request, 'audits/audit_form.html', {'form': form, 'action': 'Create'})


@login_required
def audit_execute(request, pk):
    """Execute an audit - fill in checklist responses."""
    audit = get_object_or_404(Audit, pk=pk)
    
    if request.user != audit.auditor and not request.user.is_admin_user:
        messages.error(request, 'Only the assigned auditor can execute this audit.')
        return redirect('audit_detail', pk=pk)
    
    if audit.status == 'pending':
        audit.status = 'in_progress'
        audit.started_at = timezone.now()
        audit.save()
    
    responses = audit.responses.select_related(
        'checklist_item', 'checklist_item__category'
    ).order_by('checklist_item__category__order', 'checklist_item__order')
    
    if request.method == 'POST':
        for response in responses:
            status = request.POST.get(f'status_{response.id}')
            findings = request.POST.get(f'findings_{response.id}', '')
            recommendations = request.POST.get(f'recommendations_{response.id}', '')
            
            if status:
                response.status = status
                response.findings = findings
                response.recommendations = recommendations
                response.reviewed_by = request.user
                response.reviewed_at = timezone.now()
                response.save()
        
        messages.success(request, 'Audit responses saved.')
        
        if 'complete' in request.POST:
            audit.status = 'completed'
            audit.completed_at = timezone.now()
            audit.save()
            messages.success(request, 'Audit marked as completed.')
            return redirect('audit_detail', pk=pk)
    
    return render(request, 'audits/audit_execute.html', {
        'audit': audit,
        'responses': responses,
    })


@login_required
def checklist_list(request):
    """View all checklist items organized by category."""
    categories = AuditCategory.objects.filter(is_active=True).prefetch_related(
        'checklist_items'
    )
    return render(request, 'audits/checklist_list.html', {'categories': categories})
