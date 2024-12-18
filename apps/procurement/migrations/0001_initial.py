# Generated by Django 5.0 on 2024-10-29 19:53

import apps.procurement.models.requisition
import apps.procurement.models.rfq_contract
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseOrderApproval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approve', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], max_length=255)),
                ('remarks', models.TextField(blank=True, max_length=500)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Requisition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_type', models.CharField(default='Work', max_length=100)),
                ('statement_of_requirements', models.FileField(blank=True, help_text='Max 10MB, filetypes pdf, txt, docx', null=True, upload_to=apps.procurement.models.requisition.upload_to)),
                ('approval_status', models.CharField(blank=True, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=255)),
                ('pr_status', models.CharField(blank=True, choices=[('pending', 'Pending'), ('initiating', 'Initiating'), ('processing', 'Processing'), ('rejected', 'Rejected')], default='pending', max_length=255)),
                ('remarks', models.TextField(blank=True, default='', null=True)),
                ('date_required', models.DateTimeField(auto_now_add=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='RequisitionApproval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('procurement_method', models.CharField(choices=[('single_sourcing', 'Single Sourcing'), ('rfq', 'Request For Quotations'), ('restricted_tender', 'Restricted Tender'), ('international_tender', 'International Tender'), ('not_applied', 'Not Applied'), ('rfq 2', 'Request For Quotations 2')], default='single_sourcing', max_length=255)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=255)),
                ('editable', models.BooleanField(blank=True, default=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='RequisitionItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('quantity', models.IntegerField(default=1)),
                ('measurement_unit', models.CharField(choices=[('units', 'Units'), ('pieces', 'Pieces'), ('metres', 'Metres'), ('inches', 'Inches'), ('bundles', 'Bundles'), ('bytes', 'Bytes'), ('litres', 'Litres'), ('other', 'Other')], max_length=100)),
                ('unit_cost', models.FloatField(default=4250.0, null=True)),
                ('total_cost', models.FloatField(default=4250.0, null=True)),
                ('remark', models.CharField(blank=True, max_length=100, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='RFQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='Form 101 - Requests For Quotation', help_text="The title helps with organizing and identifying your rfq's ", max_length=255)),
                ('description', models.TextField(blank=True, default='')),
                ('approval_status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=100)),
                ('open_status', models.BooleanField(default=False)),
                ('level', models.CharField(choices=[('APPROVAL LEVEL', 'Approval Level'), ('PUBLISH LEVEL', 'Publish Level'), ('QUOTATION LEVEL', 'Quotation Level'), ('EVALUATION LEVEL', 'Evaluation Level'), ('CONTRACT LEVEL', 'Contract Level'), ('PURCHASE ORDER LEVEL', 'Purchase Order Level'), ('INVOICE LEVEL', 'Invoice Level')], default='APPROVAL LEVEL', max_length=50)),
                ('quotation_deadline_date', models.DateTimeField()),
                ('terms_and_conditions', models.TextField(default='')),
                ('published', models.BooleanField(blank=True, default=False, help_text='Publish this rfq to all suppliers')),
                ('auto_publish', models.BooleanField(default=False, help_text='Auto publish the RFQ when its approved')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('-created_date',),
                'get_latest_by': '-created_date',
            },
        ),
        migrations.CreateModel(
            name='RFQApproval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approve', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=100)),
                ('editable', models.BooleanField(blank=True, default=True)),
                ('remarks', models.TextField(blank=True, default='', max_length=300)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='RFQApprovalGPPA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approve', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=100)),
                ('editable', models.BooleanField(blank=True, default=True)),
                ('remarks', models.CharField(blank=True, max_length=255, null=True)),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('last_modified', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='RFQContract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approval_status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=100)),
                ('delivery_terms', models.CharField(blank=True, max_length=100, null=True)),
                ('payment_method', models.CharField(blank=True, max_length=100, null=True)),
                ('validity_period', models.DateTimeField(blank=True, null=True)),
                ('pricing', models.DecimalField(decimal_places=2, max_digits=10)),
                ('deadline_date', models.DateTimeField(blank=True, null=True)),
                ('terms_and_conditions', models.TextField()),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('AWARDED', 'Awarded'), ('SUCCESSFUL', 'Successful'), ('PENDING', 'Pending'), ('PROCESSING', 'Processing'), ('UNSUCCESSFUL', 'Unsuccessful'), ('TERMINATED', 'Terminated')], default='PENDING', max_length=50)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='RFQContractApproval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remarks', models.TextField(blank=True, null=True)),
                ('approve', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=50)),
                ('editable', models.BooleanField(blank=True, default=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='RFQContractAward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remarks', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('AWARDED', 'Awarded'), ('SUCCESSFUL', 'Successful'), ('PENDING', 'Pending'), ('PROCESSING', 'Processing'), ('UNSUCCESSFUL', 'Unsuccessful'), ('TERMINATED', 'Terminated')], default='PENDING', max_length=50)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='RFQEvaluation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'RFQ Evaluation',
            },
        ),
        migrations.CreateModel(
            name='RFQEvaluationApprover',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approve', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], max_length=100)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='RFQItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_description', models.CharField(max_length=255)),
                ('quantity', models.IntegerField(default=1)),
                ('measurement_unit', models.CharField(choices=[('units', 'Units'), ('pieces', 'Pieces'), ('metres', 'Metres'), ('inches', 'Inches'), ('bundles', 'Bundles'), ('bytes', 'Bytes'), ('litres', 'Litres'), ('other', 'Other')], max_length=255)),
                ('remark', models.CharField(blank=True, max_length=255, null=True)),
                ('eval_criteria', models.CharField(blank=True, default='', max_length=255)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'RFQ Item',
            },
        ),
        migrations.CreateModel(
            name='RFQNegotiation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('outcome', models.TextField(blank=True, default='')),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('AWARDED', 'Awarded'), ('SUCCESSFUL', 'Successful'), ('PENDING', 'Pending'), ('PROCESSING', 'Processing'), ('UNSUCCESSFUL', 'Unsuccessful'), ('TERMINATED', 'Terminated')], default='PENDING', max_length=50)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='RFQNegotiationNote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_terms', models.CharField(max_length=100)),
                ('payment_method', models.CharField(max_length=100)),
                ('validity_period', models.DateTimeField(null=True)),
                ('pricing', models.DecimalField(decimal_places=2, max_digits=10)),
                ('accepted', models.BooleanField(default=False)),
                ('renegotiated', models.BooleanField(default=False)),
                ('note', models.TextField()),
                ('file', models.FileField(blank=True, null=True, upload_to=apps.procurement.models.rfq_contract.negotiation_notes)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'RFQ Negotiation Note',
                'ordering': ['-created_date', 'accepted'],
            },
        ),
        migrations.CreateModel(
            name='RFQQuotationEvaluation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('pricing', models.DecimalField(decimal_places=2, max_digits=10)),
                ('comments', models.TextField(blank=True, null=True)),
                ('rating', models.IntegerField(default=1)),
                ('status', models.CharField(default='pending', max_length=100)),
                ('specifications', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'RFQ Response Evaluation',
            },
        ),
        migrations.CreateModel(
            name='UnitRequisitionApproval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent_id', models.CharField(max_length=255)),
                ('approve', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='no', max_length=255)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('remark', models.TextField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WorkflowStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField()),
                ('condition_type', models.CharField(choices=[('amount_gt', 'Amount greater than'), ('amount_lt', 'Amount less than'), ('dept_eq', 'Department equals'), ('unit_eq', 'Unit equals'), ('always', 'Always execute'), ('item_count_gt', 'Item count greater than'), ('req_type_eq', 'Requisition type equals'), ('days_since_sub', 'Days since submission')], default='always', max_length=20)),
                ('condition_value', models.CharField(blank=True, max_length=255, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='ApprovalAction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('approved', 'Approved'), ('rejected', 'Rejected'), ('delegated', 'Delegated')], max_length=20)),
                ('comments', models.TextField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('approver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.staff')),
            ],
        ),
        migrations.CreateModel(
            name='ApprovalStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('order', models.IntegerField(default=1)),
                ('role', models.CharField(blank=True, help_text='Role required for this approval step', max_length=255, null=True)),
                ('is_optional', models.BooleanField(default=False)),
                ('remarks', models.TextField(blank=True, default='', max_length=1000, null=True)),
                ('is_final', models.BooleanField(default=False)),
                ('time_limit', models.DurationField(blank=True, help_text='Time limit for this approval step', null=True)),
                ('description', models.TextField(blank=True, default='', max_length=1000, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('approver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approver', to='organization.staff')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='organization.staff')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.department')),
            ],
            options={
                'ordering': ['order', '-created_date'],
            },
        ),
        migrations.CreateModel(
            name='ApprovalWorkflow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('status', models.CharField(blank=True, default='active', max_length=255, null=True)),
                ('description', models.TextField(blank=True, default='', max_length=1000, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='organization.staff')),
            ],
            options={
                'ordering': ['status', '-created_date'],
            },
        ),
        migrations.CreateModel(
            name='ApprovalMatrix',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('max_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('status', models.CharField(blank=True, default='active', max_length=25)),
                ('description', models.TextField(blank=True, default='', max_length=300, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='organization.staff')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='organization.department')),
                ('unit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='organization.unit')),
                ('workflow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='procurement.approvalworkflow')),
            ],
        ),
        migrations.CreateModel(
            name='Delegation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('reason', models.TextField(blank=True, null=True)),
                ('delegate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='delegated_to', to='organization.staff')),
                ('delegator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='delegated_from', to='organization.staff')),
            ],
        ),
        migrations.CreateModel(
            name='DepartmentRequisitionApproval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent_id', models.CharField(max_length=255)),
                ('approve', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='no', max_length=255)),
                ('remark', models.TextField(blank=True, max_length=500, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('officer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='departments_approval_officer', to='organization.staff')),
            ],
        ),
        migrations.CreateModel(
            name='FinanceRequisitionApproval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent_id', models.CharField(max_length=255)),
                ('approve', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='no', max_length=255)),
                ('remark', models.TextField(blank=True, max_length=500, null=True)),
                ('funds_confirmed', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('officer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='finance_approval_officer', to='organization.staff')),
            ],
        ),
        migrations.CreateModel(
            name='ProcurementRequisitionApproval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent_id', models.CharField(max_length=255)),
                ('approve', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], max_length=255)),
                ('part_of_annual_plan', models.BooleanField(default=False)),
                ('remark', models.TextField(blank=True, max_length=500, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('annual_procurement_plan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='organization.planitem')),
                ('officer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='procurement_departments_approval_officer', to='organization.staff')),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments', models.TextField(max_length=500)),
                ('published', models.BooleanField(default=False)),
                ('auto_publish', models.BooleanField(default=True)),
                ('requires_approval', models.BooleanField(default=True)),
                ('approval_status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=100)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('officer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.staff')),
            ],
            options={
                'ordering': ['-last_modified', '-created_date'],
            },
        ),
    ]
