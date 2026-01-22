"""
Management command to load master DPDP compliance checklist.
Run with: python manage.py load_checklist
"""
from django.core.management.base import BaseCommand
from apps.core.models import DPDPSection
from apps.audits.models import AuditCategory, ChecklistItem


class Command(BaseCommand):
    help = 'Load master DPDP compliance checklist data'

    def handle(self, *args, **options):
        self.stdout.write('Loading DPDP Sections...')
        
        # DPDP Act Sections
        sections_data = [
            ('4', 'Application of Act', 'Application of the Act to processing of digital personal data.'),
            ('5', 'Lawful Processing', 'Processing of personal data for a lawful purpose.'),
            ('6', 'Consent', 'Processing of personal data based on consent of data principal.'),
            ('7', 'Certain Legitimate Uses', 'Processing for certain legitimate uses without consent.'),
            ('8', 'General Obligations of Data Fiduciary', 'Obligations of data fiduciary including security and breach notification.'),
            ('9', 'Additional Obligations for Children', 'Additional obligations for processing personal data of children.'),
            ('10', 'Significant Data Fiduciary', 'Additional obligations for significant data fiduciaries.'),
            ('11', 'Rights and Duties of Data Principal', 'Rights of data principals and their duties.'),
            ('12', 'Right to Information', 'Right to obtain information about personal data processing.'),
            ('13', 'Right to Correction and Erasure', 'Right to correction, completion, updating and erasure.'),
            ('14', 'Right of Grievance Redressal', 'Right to have grievances addressed.'),
            ('15', 'Right to Nominate', 'Right to nominate another person to exercise rights.'),
            ('16', 'Transfer of Personal Data Outside India', 'Provisions for cross-border data transfer.'),
            ('17', 'Exemptions', 'Exemptions from provisions of the Act.'),
        ]
        
        sections = {}
        for num, title, desc in sections_data:
            section, created = DPDPSection.objects.get_or_create(
                section_number=num,
                defaults={'title': title, 'description': desc}
            )
            sections[num] = section
            if created:
                self.stdout.write(f'  Created Section {num}')
        
        self.stdout.write(self.style.SUCCESS('DPDP Sections loaded'))
        
        # Audit Categories (Modules)
        self.stdout.write('Loading Audit Categories...')
        
        categories_data = [
            ('Data Collection & Consent Management', 'Compliance requirements for lawful collection and obtaining valid consent.', '6', 1),
            ('Purpose Limitation & Data Minimization', 'Using data only for specified purposes and collecting only necessary data.', '5', 2),
            ('Data Fiduciary Obligations', 'Security measures, accuracy, retention, and breach notification.', '8', 3),
            ('Children\'s Data Protection', 'Special protections for processing personal data of children.', '9', 4),
            ('Data Principal Rights', 'Implementation of rights to access, correction, erasure, and portability.', '11', 5),
            ('Significant Data Fiduciary Compliance', 'Additional obligations for significant data fiduciaries.', '10', 6),
            ('Cross-Border Data Transfer', 'Compliance with data localization and transfer requirements.', '16', 7),
            ('Grievance Redressal Mechanism', 'Procedures for addressing data principal grievances.', '14', 8),
        ]
        
        categories = {}
        for name, desc, section_num, order in categories_data:
            cat, created = AuditCategory.objects.get_or_create(
                name=name,
                defaults={
                    'description': desc,
                    'dpdp_section': sections.get(section_num),
                    'order': order
                }
            )
            categories[name] = cat
            if created:
                self.stdout.write(f'  Created Category: {name}')
        
        self.stdout.write(self.style.SUCCESS('Audit Categories loaded'))
        
        # Checklist Items
        self.stdout.write('Loading Checklist Items...')
        
        checklist_items = [
            # Data Collection & Consent Management
            ('DC-001', 'Consent Notice Clarity', 'Clear, specific consent notice provided in plain language before data collection.', 
             'Verify consent notice is displayed, understandable, and explains data usage clearly.', 
             'Screenshots of consent UI, consent notice text', 'critical', 'Data Collection & Consent Management', 1),
            ('DC-002', 'Affirmative Consent Action', 'Consent obtained through affirmative action, not pre-ticked boxes or silence.', 
             'Check consent mechanism requires explicit action by user.', 
             'UI screenshots, user flow documentation', 'critical', 'Data Collection & Consent Management', 2),
            ('DC-003', 'Consent Withdrawal Mechanism', 'Easy mechanism for withdrawing consent with equal prominence as giving consent.', 
             'Verify withdrawal option is accessible and effective.', 
             'Withdrawal flow screenshots, user journey', 'critical', 'Data Collection & Consent Management', 3),
            ('DC-004', 'Consent Records Maintenance', 'Records of consent with timestamp and scope maintained securely.', 
             'Review consent logging and record-keeping practices.', 
             'Consent database schema, sample records', 'major', 'Data Collection & Consent Management', 4),
            ('DC-005', 'Bundled Consent Separation', 'Consent for different purposes not bundled together inappropriately.', 
             'Check if separate consents are obtained for distinct processing activities.', 
             'Consent form design, processing activity mapping', 'major', 'Data Collection & Consent Management', 5),
            
            # Purpose Limitation & Data Minimization
            ('PL-001', 'Specified Purpose Documentation', 'All purposes for data collection clearly documented and communicated.', 
             'Review privacy policy and consent notices for purpose specification.', 
             'Privacy policy, purpose inventory', 'critical', 'Purpose Limitation & Data Minimization', 1),
            ('PL-002', 'Purpose Limitation Controls', 'Technical controls preventing use of data beyond specified purposes.', 
             'Verify access controls and data usage monitoring.', 
             'Access control policies, data usage logs', 'major', 'Purpose Limitation & Data Minimization', 2),
            ('PL-003', 'Data Minimization Implementation', 'Only necessary personal data collected for the specified purpose.', 
             'Audit data fields collected against stated purposes.', 
             'Data mapping, collection forms', 'major', 'Purpose Limitation & Data Minimization', 3),
            
            # Data Fiduciary Obligations
            ('DF-001', 'Security Safeguards Implementation', 'Reasonable security safeguards implemented to prevent data breaches.', 
             'Review security measures including encryption, access controls, monitoring.', 
             'Security policy, encryption certificates, penetration test reports', 'critical', 'Data Fiduciary Obligations', 1),
            ('DF-002', 'Data Accuracy Procedures', 'Procedures to ensure personal data is accurate, complete, and up-to-date.', 
             'Check data validation and update mechanisms.', 
             'Data quality procedures, validation rules', 'major', 'Data Fiduciary Obligations', 2),
            ('DF-003', 'Data Retention Policy', 'Data retention periods defined and enforced, data deleted when no longer needed.', 
             'Review retention policy and deletion procedures.', 
             'Retention schedule, deletion logs', 'major', 'Data Fiduciary Obligations', 3),
            ('DF-004', 'Breach Notification Procedures', 'Procedures to notify Board and affected individuals of data breach.', 
             'Verify incident response and notification procedures.', 
             'Incident response plan, notification templates', 'critical', 'Data Fiduciary Obligations', 4),
            ('DF-005', 'Data Processor Agreements', 'Contractual agreements with data processors ensuring compliance.', 
             'Review contracts with third-party processors.', 
             'Processor agreements, vendor assessments', 'major', 'Data Fiduciary Obligations', 5),
            
            # Children's Data Protection
            ('CD-001', 'Age Verification Mechanism', 'Verifiable age verification before collecting children\'s data.', 
             'Check age gate implementation and verification methods.', 
             'Age verification UI, verification logic', 'critical', 'Children\'s Data Protection', 1),
            ('CD-002', 'Verifiable Parental Consent', 'Verifiable consent from parent/guardian obtained for children.', 
             'Verify parental consent workflow and verification.', 
             'Parental consent forms, verification process', 'critical', 'Children\'s Data Protection', 2),
            ('CD-003', 'No Behavioral Tracking', 'No tracking, behavioral monitoring, or targeted advertising for children.', 
             'Verify analytics and ad systems exclude children.', 
             'Analytics configuration, ad policies', 'critical', 'Children\'s Data Protection', 3),
            ('CD-004', 'No Detrimental Processing', 'Processing does not cause detrimental effects on child\'s well-being.', 
             'Review processing activities for potential harm.', 
             'Impact assessment, content policies', 'major', 'Children\'s Data Protection', 4),
            
            # Data Principal Rights
            ('DP-001', 'Right to Access Implementation', 'Data principals can access their personal data and processing details.', 
             'Test data access request mechanism.', 
             'Access request form, response samples', 'critical', 'Data Principal Rights', 1),
            ('DP-002', 'Right to Correction', 'Mechanism for correction, completion, and updating of personal data.', 
             'Verify data correction functionality.', 
             'Profile edit UI, correction request process', 'major', 'Data Principal Rights', 2),
            ('DP-003', 'Right to Erasure', 'Mechanism for data erasure with appropriate retention exceptions.', 
             'Test account deletion and data erasure process.', 
             'Deletion flow, erasure verification', 'major', 'Data Principal Rights', 3),
            ('DP-004', 'Response Timeline Compliance', 'Rights requests responded to within prescribed timelines.', 
             'Review SLAs and response time tracking.', 
             'SLA documentation, response time metrics', 'major', 'Data Principal Rights', 4),
            
            # Significant Data Fiduciary
            ('SD-001', 'DPO Appointment', 'Data Protection Officer appointed and contact details published.', 
             'Verify DPO appointment and public availability of contact.', 
             'DPO appointment letter, published contact', 'critical', 'Significant Data Fiduciary Compliance', 1),
            ('SD-002', 'Independent Auditor', 'Independent data auditor appointed for periodic audits.', 
             'Check auditor appointment and audit schedule.', 
             'Auditor contract, audit reports', 'critical', 'Significant Data Fiduciary Compliance', 2),
            ('SD-003', 'Data Protection Impact Assessment', 'DPIA conducted for high-risk processing activities.', 
             'Review DPIA documentation.', 
             'DPIA reports, risk assessments', 'major', 'Significant Data Fiduciary Compliance', 3),
            
            # Cross-Border Data Transfer
            ('CB-001', 'Transfer Restriction Compliance', 'Personal data not transferred to restricted territories.', 
             'Verify data storage locations and transfer destinations.', 
             'Data flow maps, hosting documentation', 'critical', 'Cross-Border Data Transfer', 1),
            ('CB-002', 'Government Notification', 'Central Government notified of specified data transfers.', 
             'Check notification compliance for cross-border transfers.', 
             'Transfer notifications, government approvals', 'major', 'Cross-Border Data Transfer', 2),
            
            # Grievance Redressal
            ('GR-001', 'Grievance Officer Appointment', 'Grievance redressal officer appointed with published contact.', 
             'Verify officer appointment and contact availability.', 
             'Appointment documentation, contact details', 'critical', 'Grievance Redressal Mechanism', 1),
            ('GR-002', 'Grievance Resolution Timeline', 'Grievances resolved within prescribed timelines.', 
             'Review grievance handling SLAs and metrics.', 
             'SLA documentation, resolution metrics', 'major', 'Grievance Redressal Mechanism', 2),
            ('GR-003', 'Grievance Tracking System', 'System for logging and tracking grievances to resolution.', 
             'Verify grievance management system.', 
             'Ticketing system, tracking reports', 'major', 'Grievance Redressal Mechanism', 3),
        ]
        
        for code, title, desc, guidance, evidence, severity, cat_name, order in checklist_items:
            item, created = ChecklistItem.objects.get_or_create(
                code=code,
                defaults={
                    'title': title,
                    'description': desc,
                    'guidance': guidance,
                    'evidence_required': evidence,
                    'severity': severity,
                    'category': categories[cat_name],
                    'order': order
                }
            )
            if created:
                self.stdout.write(f'  Created: {code} - {title}')
        
        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {len(checklist_items)} checklist items'))
        self.stdout.write(self.style.SUCCESS('Master DPDP checklist data loaded successfully!'))
