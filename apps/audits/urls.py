"""
URL patterns for audits app.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.audit_list, name='audit_list'),
    path('create/', views.audit_create, name='audit_create'),
    path('<int:pk>/', views.audit_detail, name='audit_detail'),
    path('<int:pk>/execute/', views.audit_execute, name='audit_execute'),
    path('checklist/', views.checklist_list, name='checklist_list'),
]
