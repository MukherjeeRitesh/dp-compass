"""
Audit forms for creating and managing audits.
"""
from django import forms
from .models import Audit, AuditResponse


class AuditForm(forms.ModelForm):
    """Form for creating/editing audits."""
    
    class Meta:
        model = Audit
        fields = ['application', 'title', 'description', 'scheduled_date']
        widgets = {
            'scheduled_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class AuditResponseForm(forms.ModelForm):
    """Form for audit responses."""
    
    class Meta:
        model = AuditResponse
        fields = ['status', 'findings', 'evidence_notes', 'recommendations']
        widgets = {
            'findings': forms.Textarea(attrs={'rows': 2}),
            'evidence_notes': forms.Textarea(attrs={'rows': 2}),
            'recommendations': forms.Textarea(attrs={'rows': 2}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
