# Generated by Django 5.0 on 2024-09-28 16:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='authgroup',
            options={'ordering': ['-last_modified', '-created_date'], 'verbose_name': 'Authorization Group'},
        ),
    ]
