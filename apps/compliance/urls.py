"""
URL patterns for compliance app.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('applications/', views.application_list, name='application_list'),
    path('applications/create/', views.application_create, name='application_create'),
    path('applications/<int:pk>/', views.application_detail, name='application_detail'),
    path('applications/<int:pk>/edit/', views.application_edit, name='application_edit'),
    path('remediations/', views.remediation_list, name='remediation_list'),
    path('remediations/<int:pk>/', views.remediation_detail, name='remediation_detail'),
]
