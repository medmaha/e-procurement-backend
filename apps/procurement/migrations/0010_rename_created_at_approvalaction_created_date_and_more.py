# Generated by Django 5.0 on 2024-10-24 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('procurement', '0009_approvalstep_description_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='approvalaction',
            old_name='created_at',
            new_name='created_date',
        ),
        migrations.RenameField(
            model_name='approvalstep',
            old_name='officer',
            new_name='approver',
        ),
        migrations.RemoveField(
            model_name='workflowstep',
            name='condition',
        ),
        migrations.AddField(
            model_name='approvalaction',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='workflowstep',
            name='condition_type',
            field=models.CharField(choices=[('amount_gt', 'Amount greater than'), ('amount_lt', 'Amount less than'), ('dept_eq', 'Department equals'), ('unit_eq', 'Unit equals'), ('always', 'Always execute'), ('item_count_gt', 'Item count greater than'), ('req_type_eq', 'Requisition type equals'), ('days_since_sub', 'Days since submission')], default='always', max_length=20),
        ),
        migrations.AddField(
            model_name='workflowstep',
            name='condition_value',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
