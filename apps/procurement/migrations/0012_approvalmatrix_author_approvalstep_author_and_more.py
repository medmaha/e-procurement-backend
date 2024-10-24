# Generated by Django 5.0 on 2024-10-24 10:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0003_unit_email_alter_staff_is_admin_and_more'),
        ('procurement', '0011_rename_officer_approvalworkflow_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='approvalmatrix',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='organization.staff'),
        ),
        migrations.AddField(
            model_name='approvalstep',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='organization.staff'),
        ),
        migrations.AddField(
            model_name='workflowstep',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='organization.staff'),
        ),
        migrations.AlterField(
            model_name='approvalstep',
            name='approver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approver', to='organization.staff'),
        ),
    ]
