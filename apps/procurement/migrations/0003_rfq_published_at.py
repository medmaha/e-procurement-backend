# Generated by Django 5.0 on 2024-10-30 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('procurement', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rfq',
            name='published_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
