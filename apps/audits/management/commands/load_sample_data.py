"""
Management command to load sample demo data.
Run with: python manage.py load_sample_data
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.users.models import User
from apps.compliance.models import Application
from apps.audits.models import Audit, AuditResponse, ChecklistItem


class Command(BaseCommand):
    help = 'Load sample demo data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create or get admin user
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@dpcompass.local',
                'first_name': 'System',
                'last_name': 'Administrator',
                'role': 'admin',
                'organization': 'DP-COMPASS',
                'is_verified': True,
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin.set_password('Admin@123')
            admin.save()
            self.stdout.write('  Created admin: admin / Admin@123')
        else:
            admin.role = 'admin'
            admin.first_name = 'System'
            admin.last_name = 'Administrator'
            admin.organization = 'DP-COMPASS'
            admin.is_verified = True
            admin.save()
            self.stdout.write('  Updated admin user')
        
        # Create an auditor
        auditor, created = User.objects.get_or_create(
            username='auditor',
            defaults={
                'email': 'auditor@dpcompass.local',
                'first_name': 'Priya',
                'last_name': 'Sharma',
                'role': 'auditor',
                'organization': 'Compliance Team',
                'designation': 'Senior Compliance Auditor',
                'is_verified': True,
            }
        )
        if created:
            auditor.set_password('Auditor@123')
            auditor.save()
            self.stdout.write('  Created auditor: auditor / Auditor@123')
        
        # Create a developer
        developer, created = User.objects.get_or_create(
            username='developer',
            defaults={
                'email': 'developer@dpcompass.local',
                'first_name': 'Rahul',
                'last_name': 'Kumar',
                'role': 'developer',
                'organization': 'Engineering Team',
                'designation': 'Tech Lead',
                'is_verified': True,
            }
        )
        if created:
            developer.set_password('Developer@123')
            developer.save()
            self.stdout.write('  Created developer: developer / Developer@123')
        
        # Create sample applications
        apps_data = [
            {
                'name': 'Customer Portal',
                'description': 'Main customer-facing web portal for account management, transactions, and support.',
                'application_type': 'web',
                'environment': 'production',
                'department': 'Digital Services',
                'url': 'https://portal.example.com',
                'version': '3.2.1',
                'data_categories': 'Customer PII (name, email, phone), Financial data, Transaction history, Support tickets',
            },
            {
                'name': 'Mobile Banking App',
                'description': 'iOS and Android mobile banking application with biometric authentication.',
                'application_type': 'mobile',
                'environment': 'production',
                'department': 'Mobile Development',
                'version': '2.5.0',
                'data_categories': 'Customer PII, Biometric data, Location data, Device identifiers, Transaction data',
            },
            {
                'name': 'HR Management System',
                'description': 'Internal HR system for employee data, payroll, and performance management.',
                'application_type': 'web',
                'environment': 'production',
                'department': 'Human Resources',
                'version': '1.8.3',
                'data_categories': 'Employee PII, Salary data, Performance reviews, Medical records',
            },
        ]
        
        applications = []
        for app_data in apps_data:
            app, created = Application.objects.get_or_create(
                name=app_data['name'],
                defaults={**app_data, 'owner': developer}
            )
            applications.append(app)
            if created:
                self.stdout.write(f'  Created application: {app.name}')
        
        # Create sample audits
        audit1, created = Audit.objects.get_or_create(
            title='Q1 2026 Compliance Audit - Customer Portal',
            application=applications[0],
            defaults={
                'description': 'Quarterly DPDP compliance assessment for Customer Portal',
                'auditor': auditor,
                'status': 'pending',
                'scheduled_date': timezone.now().date(),
            }
        )
        
        if created:
            # Create audit responses for all checklist items
            checklist_items = ChecklistItem.objects.filter(is_active=True)
            for item in checklist_items:
                AuditResponse.objects.create(
                    audit=audit1,
                    checklist_item=item,
                    status='pending'
                )
            self.stdout.write(f'  Created audit: {audit1.title} with {checklist_items.count()} checklist items')
        
        # Create a completed audit for HR System
        audit2, created = Audit.objects.get_or_create(
            title='Initial Assessment - HR Management System',
            application=applications[2],
            defaults={
                'description': 'Initial DPDP compliance baseline assessment',
                'auditor': auditor,
                'status': 'completed',
                'scheduled_date': timezone.now().date(),
                'started_at': timezone.now(),
                'completed_at': timezone.now(),
            }
        )
        
        if created:
            # Create audit responses with mixed statuses
            checklist_items = ChecklistItem.objects.filter(is_active=True)
            statuses = ['compliant', 'compliant', 'non_compliant', 'partially_compliant', 'compliant']
            for i, item in enumerate(checklist_items):
                status = statuses[i % len(statuses)]
                AuditResponse.objects.create(
                    audit=audit2,
                    checklist_item=item,
                    status=status,
                    findings=f'Assessment findings for {item.code}',
                    reviewed_by=auditor,
                    reviewed_at=timezone.now()
                )
            self.stdout.write(f'  Created completed audit: {audit2.title}')
        
        self.stdout.write(self.style.SUCCESS('\nSample data loaded successfully!'))
        self.stdout.write('\nTest Accounts:')
        self.stdout.write('  Admin:     admin / Admin@123')
        self.stdout.write('  Auditor:   auditor / Auditor@123')
        self.stdout.write('  Developer: developer / Developer@123')

