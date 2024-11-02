# Generated by Django 5.0 on 2024-11-02 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0006_alter_rfqresponse_evaluation_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rfqresponse',
            name='evaluation_status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('AWARDED', 'Awarded'), ('REJECTED', 'Rejected'), ('EVALUATED', 'Evaluated'), ('AWARD_AWAITING_APPROVAL', 'Await Await')], default='PENDING', help_text='Whether vendor accepts or rejects this requisition', max_length=50),
        ),
    ]