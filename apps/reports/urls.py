"""
URL patterns for reports app.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.report_list, name='report_list'),
    path('<int:pk>/', views.report_detail, name='report_detail'),
    path('generate/<int:audit_id>/', views.report_generate, name='report_generate'),
    path('<int:pk>/export/', views.report_export_pdf, name='report_export_pdf'),
    path('<int:pk>/approve/', views.report_approve, name='report_approve'),
]
