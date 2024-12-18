# Generated by Django 5.0 on 2024-11-02 02:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('procurement', '0004_contractaward_contractawardapproval'),
        ('vendors', '0004_vendor_short_desc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contractaward',
            name='quotation',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='vendors.rfqresponse'),
        ),
        migrations.AlterField(
            model_name='contractawardapproval',
            name='award',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='approval', to='procurement.contractaward'),
        ),
        migrations.AlterField(
            model_name='rfq',
            name='level',
            field=models.CharField(choices=[('APPROVAL LEVEL', 'Approval Level'), ('PUBLISH LEVEL', 'Publish Level'), ('QUOTATION LEVEL', 'Quotation Level'), ('EVALUATION LEVEL', 'Evaluation Level'), ('AWARD LEVEL', 'Award Level'), ('CONTRACT LEVEL', 'Contract Level'), ('PURCHASE ORDER LEVEL', 'Purchase Order Level'), ('INVOICE LEVEL', 'Invoice Level')], default='APPROVAL LEVEL', max_length=50),
        ),
    ]
