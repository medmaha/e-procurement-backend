# Generated by Django 5.0 on 2024-10-24 07:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('procurement', '0010_rename_created_at_approvalaction_created_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='approvalworkflow',
            old_name='officer',
            new_name='author',
        ),
    ]
