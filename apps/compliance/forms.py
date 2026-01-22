"""
Compliance forms for application and remediation management.
"""
from django import forms
from .models import Application, Remediation


class ApplicationForm(forms.ModelForm):
    """Form for registering/editing applications."""
    
    class Meta:
        model = Application
        fields = [
            'name', 'description', 'application_type', 'environment',
            'owner', 'department', 'url', 'version', 'data_categories'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'data_categories': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class RemediationForm(forms.ModelForm):
    """Form for managing remediations."""
    
    class Meta:
        model = Remediation
        fields = [
            'title', 'description', 'status', 'priority',
            'assigned_to', 'due_date', 'resolution_notes'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'resolution_notes': forms.Textarea(attrs={'rows': 3}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
