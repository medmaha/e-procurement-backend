# Generated by Django 5.0 on 2024-11-03 13:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0001_initial'),
        ('procurement', '0008_contract_attachments'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='approval_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=100),
        ),
        migrations.AddField(
            model_name='contract',
            name='officer',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='created_contracts', to='organization.staff'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contract',
            name='terminated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='terminated_contracts', to='organization.staff'),
        ),
        migrations.AddField(
            model_name='contract',
            name='terminated_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contract',
            name='terminated_reason',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.DeleteModel(
            name='ContractTermination',
        ),
    ]