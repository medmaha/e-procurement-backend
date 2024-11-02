# Generated by Django 5.0 on 2024-11-03 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('procurement', '0006_contractdocument_contract_contracttermination'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContractAttachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('document_url', models.CharField(max_length=1000)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='contract',
            name='additional_documents',
        ),
        migrations.RemoveField(
            model_name='contract',
            name='contract_document',
        ),
        migrations.DeleteModel(
            name='ContractDocument',
        ),
    ]