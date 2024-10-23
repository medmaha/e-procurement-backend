# Generated by Django 5.0 on 2024-10-23 15:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0003_unit_email_alter_staff_is_admin_and_more'),
        ('procurement', '0007_workflowstep_created_date_workflowstep_last_modified'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='approvalstep',
            options={'ordering': ['order', '-id']},
        ),
        migrations.AddField(
            model_name='approvalstep',
            name='officer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='organization.staff'),
        ),
        migrations.AddField(
            model_name='approvalworkflow',
            name='officer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='organization.staff'),
        ),
    ]