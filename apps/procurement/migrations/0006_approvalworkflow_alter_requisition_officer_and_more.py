# Generated by Django 5.0 on 2024-10-22 22:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_alter_threshold_procurement_method'),
        ('procurement', '0005_requisition_officer_department_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApprovalWorkflow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='requisition',
            name='officer',
            field=models.ForeignKey(blank=True, help_text='Authorizes this instance', on_delete=django.db.models.deletion.CASCADE, to='organization.staff'),
        ),
        migrations.CreateModel(
            name='ApprovalStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('order', models.IntegerField()),
                ('role', models.CharField(help_text='Role required for this approval step', max_length=255)),
                ('is_optional', models.BooleanField(default=False)),
                ('remarks', models.TextField(blank=True, default='', max_length=1000, null=True)),
                ('is_final', models.BooleanField(default=False)),
                ('time_limit', models.DurationField(blank=True, help_text='Time limit for this approval step', null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.department')),
            ],
        ),
        migrations.CreateModel(
            name='ApprovalAction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('approved', 'Approved'), ('rejected', 'Rejected'), ('delegated', 'Delegated')], max_length=20)),
                ('comments', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('approver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.staff')),
                ('requisition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='approval_actions', to='procurement.requisition')),
                ('step', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='procurement.approvalstep')),
            ],
        ),
        migrations.AddField(
            model_name='requisition',
            name='current_approval_step',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='procurement.approvalstep'),
        ),
        migrations.CreateModel(
            name='ApprovalMatrix',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('max_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
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
            name='WorkflowStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField()),
                ('condition', models.TextField(blank=True, help_text='Python code for conditional execution', null=True)),
                ('step', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='procurement.approvalstep')),
                ('workflow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='procurement.approvalworkflow')),
            ],
            options={
                'ordering': ['order'],
                'unique_together': {('workflow', 'order')},
            },
        ),
        migrations.AddField(
            model_name='approvalworkflow',
            name='steps',
            field=models.ManyToManyField(related_name='workflows', through='procurement.WorkflowStep', to='procurement.approvalstep'),
        ),
    ]
