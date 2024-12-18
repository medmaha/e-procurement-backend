# Generated by Django 5.0 on 2024-10-29 19:53

import apps.vendors.models.certificate
import apps.vendors.models.rfq_response
import django.db.models.deletion
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('organization', '0001_initial'),
        ('procurement', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=100)),
                ('achieved_from', models.CharField(max_length=100)),
                ('date_achieved', models.DateField(auto_now_add=True)),
                ('verified', models.BooleanField(default=False)),
                ('file', models.FileField(null=True, upload_to=apps.vendors.models.certificate.upload_company_certificates)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_date', 'name'],
            },
        ),
        migrations.CreateModel(
            name='ContactPerson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('phone_number', models.CharField(max_length=255)),
                ('verified', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.address')),
            ],
            options={
                'verbose_name': 'Contact Person',
                'ordering': ['-created_date', '-last_modified', 'verified'],
            },
        ),
        migrations.CreateModel(
            name='RFQResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', help_text='Whether vendor accepted this requisition or rejects it', max_length=10)),
                ('proforma', models.FileField(null=True, upload_to=apps.vendors.models.rfq_response.upload_proforma)),
                ('form101', models.FileField(blank=True, null=True, upload_to=apps.vendors.models.rfq_response.upload_form101)),
                ('delivery_terms', models.CharField(max_length=100)),
                ('payment_method', models.CharField(blank=True, max_length=100, null=True)),
                ('pricing', models.DecimalField(decimal_places=2, max_digits=10)),
                ('validity_period', models.CharField(max_length=50)),
                ('remarks', models.TextField(blank=True, default='', max_length=2500)),
                ('approved_date', models.DateField(blank=True, null=True)),
                ('approved_remarks', models.TextField(blank=True, max_length=2500, null=True)),
                ('approved_status', models.CharField(choices=[('accepted', 'Accepted'), ('rejected', 'Rejected'), ('processing', 'Processing')], default='processing', help_text='Whether vendor accepted this requisition or rejects it', max_length=15)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('approved_officer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='organization.staff')),
                ('rfq', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='procurement.rfq')),
            ],
            options={
                'verbose_name': 'RFQ Response',
                'verbose_name_plural': 'RFQ Responses',
                'ordering': ['-created_date', '-last_modified'],
            },
        ),
        migrations.CreateModel(
            name='RFQResponseBrochure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('file', models.FileField(null=True, upload_to=apps.vendors.models.rfq_response.upload_brochure)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('rfq_response', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendors.rfqresponse')),
            ],
        ),
        migrations.AddField(
            model_name='rfqresponse',
            name='brochures',
            field=models.ManyToManyField(blank=True, to='vendors.rfqresponsebrochure'),
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization_name', models.CharField(max_length=255, unique=True)),
                ('alias', models.CharField(blank=True, max_length=100, null=True)),
                ('registration_type', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('tin_number', models.CharField(max_length=255)),
                ('vat_number', models.CharField(max_length=255)),
                ('license_number', models.CharField(max_length=255)),
                ('industry', models.CharField(blank=True, default='N/A', max_length=255)),
                ('website', models.URLField(blank=True, null=True)),
                ('logo', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, max_length=1000, null=True)),
                ('established_date', models.DateField(blank=True, null=True)),
                ('active', models.BooleanField(blank=True, default=False, null=True)),
                ('verified', models.BooleanField(blank=True, default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.address')),
                ('certificates', models.ManyToManyField(blank=True, related_name='vendors', to='vendors.certificate')),
                ('contact_person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vendors', to='vendors.contactperson')),
                ('user_account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vendor_account', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Vendor',
                'ordering': ['-created_date', '-last_modified', 'verified', 'active'],
            },
        ),
        migrations.AddField(
            model_name='rfqresponse',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rfq_responses', to='vendors.vendor'),
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tax_amount', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('notes', models.TextField(blank=True, default='')),
                ('due_date', models.DateField()),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('payment_terms', models.CharField(blank=True, choices=[('net_30', 'Net 30 Days'), ('net_60', 'Net 60 Days'), ('net_90', 'Net 90 Days'), ('due_on_receipt', 'Due on Receipt'), ('custom', 'Custom')], default='net_30', max_length=20)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('paid', 'Paid'), ('late', 'Late'), ('cancelled', 'Cancelled')], default='pending', max_length=20)),
                ('purchase_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='procurement.purchaseorder')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendors.vendor')),
            ],
        ),
        migrations.AddField(
            model_name='certificate',
            name='vendor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='certificate_sets', to='vendors.vendor'),
        ),
        migrations.CreateModel(
            name='VendorRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('inactive', 'Inactive'), ('active', 'Active')], default='inactive', max_length=255)),
                ('is_validated', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('vendor', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='vendors.vendor')),
            ],
            options={
                'verbose_name': 'Vendor Registration',
                'verbose_name_plural': 'Vendor Registration',
                'ordering': ['-created_date', '-last_modified', 'status'],
            },
        ),
    ]
