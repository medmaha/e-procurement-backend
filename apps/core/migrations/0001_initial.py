# Generated by Django 5.0 on 2024-10-29 19:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=255)),
                ('region', models.CharField(blank=True, max_length=255, null=True)),
                ('district', models.CharField(blank=True, max_length=255, null=True)),
                ('town', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(default='', max_length=255)),
                ('is_read', models.BooleanField(default=False)),
                ('page_url', models.URLField(max_length=255, null=True)),
                ('img_url', models.CharField(default='', max_length=255)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NotificationBatch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_seen', models.BooleanField(db_index=True, default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('notifications', models.ManyToManyField(related_name='batch', related_query_name='batch', to='core.notification')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notification_batch', related_query_name='notification_batch', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
