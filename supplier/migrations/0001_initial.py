# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address_title', models.CharField(max_length=200, null=True, blank=True)),
                ('address', models.CharField(max_length=200, null=True, blank=True)),
                ('country', models.CharField(max_length=50, null=True, blank=True)),
                ('city', models.CharField(max_length=50, null=True, blank=True)),
                ('state', models.CharField(max_length=50, null=True, blank=True)),
                ('zip_code', models.CharField(max_length=50, null=True, blank=True)),
                ('address_type', models.CharField(max_length=5, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BusinessCertificate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50, null=True, blank=True)),
                ('description', models.TextField(max_length=500, null=True, blank=True)),
                ('upload_file', models.FileField(upload_to=b'/media/certificate/')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('company_name', models.CharField(max_length=50, null=True, verbose_name=b'Company Name', blank=True)),
                ('login_url', models.URLField(max_length=256, null=True, verbose_name=b'Login Url', blank=True)),
                ('registration_url', models.URLField(max_length=256, null=True, verbose_name=b'Registration Url', blank=True)),
                ('buyer_introduction', models.CharField(max_length=500, null=True, verbose_name=b'Buyer Introduction', blank=True)),
                ('state', models.CharField(max_length=100, null=True, verbose_name=b'State', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CertificateName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cert_name', models.CharField(max_length=50, null=True, blank=True)),
                ('display_order', models.IntegerField(null=True, blank=True)),
                ('active', models.BooleanField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompanyCapabilityStatement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('capability_statement', models.TextField(max_length=250, null=True, verbose_name=b'Capability Statement', blank=True)),
                ('upload_doc', models.FileField(upload_to=b'attachment/doc', null=True, verbose_name=b'Document Upload', blank=True)),
                ('upload_video', models.CharField(max_length=250, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompanyCertification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=200, null=True, blank=True)),
                ('cert_number', models.CharField(max_length=50, null=True, blank=True)),
                ('category', models.CharField(max_length=100, null=True, blank=True)),
                ('certification_date', models.DateField(null=True, blank=True)),
                ('expire_date', models.DateField(null=True, blank=True)),
                ('certificate_duration', models.CharField(max_length=50, null=True, blank=True)),
                ('upload_certificate', models.FileField(null=True, upload_to=b'/media/certification/', blank=True)),
                ('certificate_name', models.OneToOneField(related_name='company-cert', to='supplier.CertificateName')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompanyContact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, null=True, blank=True)),
                ('title', models.CharField(max_length=50, null=True, blank=True)),
                ('phone', models.CharField(max_length=20, null=True, blank=True)),
                ('phone_ext', models.CharField(max_length=5, null=True, blank=True)),
                ('fax', models.CharField(max_length=20, null=True, blank=True)),
                ('email', models.CharField(max_length=100, null=True, blank=True)),
                ('contact_type', models.CharField(blank=True, max_length=5, null=True, choices=[(0, b'Primary'), (1, b'Secondary'), (2, b'Preparer')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompanyOwner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, null=True, blank=True)),
                ('title', models.CharField(max_length=50, null=True, blank=True)),
                ('email', models.CharField(max_length=100, null=True, blank=True)),
                ('gender', models.CharField(blank=True, max_length=10, null=True, choices=[(b'male', b'Male'), (b'female', b'Female')])),
                ('ethnicity', models.CharField(blank=True, max_length=100, null=True, choices=[(0, b'African American'), (1, b'Native American'), (2, b'Asia Pacific American'), (3, b'Subcontinent Asian American'), (4, b'Canadian Aboriginal'), (5, b'White (not Hisponic'), (6, b'Hisponic American')])),
                ('percent_ownership', models.DecimalField(default=Decimal('0.00'), max_digits=10, decimal_places=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompanyProductService',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('naics_code', models.CharField(max_length=200, null=True, blank=True)),
                ('sic_code', models.CharField(max_length=200, null=True, blank=True)),
                ('unspsc_code', models.CharField(max_length=200, null=True, blank=True)),
                ('nigp_code', models.CharField(max_length=200, null=True, blank=True)),
                ('cage_code', models.CharField(max_length=200, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompanyRevenue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_year_annual_sale', models.CharField(max_length=10, null=True, blank=True)),
                ('two_year_before_annual_sale', models.CharField(max_length=10, null=True, blank=True)),
                ('three_year_before_annual_sale', models.CharField(max_length=10, null=True, blank=True)),
                ('is_company_diverse', models.NullBooleanField(default=None)),
                ('is_company_publicly_traded', models.NullBooleanField(default=None)),
                ('is_sba', models.NullBooleanField(default=None)),
                ('minority_owned', models.NullBooleanField(default=None)),
                ('veteron_owned', models.NullBooleanField(default=None)),
                ('us_citizen_owned', models.NullBooleanField(default=None)),
                ('woman_owned', models.NullBooleanField(default=None)),
                ('service_disabled_vet', models.NullBooleanField(default=None)),
                ('owners_ethnicities', models.CharField(max_length=5, null=True, blank=True)),
                ('remit_to_email', models.CharField(max_length=50, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductAndServiceCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category_name', models.CharField(max_length=256, null=True, verbose_name=b'Category Name', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductServiceCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=50, unique=True, null=True, verbose_name=b'Code', blank=True)),
                ('code_type', models.CharField(blank=True, max_length=15, null=True, verbose_name=b'Code Type', choices=[(b'naics', b'NAICS'), (b'sic', b'SIC'), (b'unspsc', b'UNSPSC'), (b'nigp', b'NIGP'), (b'cage', b'CAGE')])),
                ('title', models.CharField(max_length=50, null=True, verbose_name=b'Title', blank=True)),
                ('common_keywords', models.CharField(max_length=200, null=True, verbose_name=b'Common Keywords', blank=True)),
                ('category', models.ForeignKey(blank=True, to='supplier.ProductAndServiceCategory', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('company_name', models.CharField(max_length=200, null=True, blank=True)),
                ('contact_name', models.CharField(max_length=200, null=True, blank=True)),
                ('phone', models.CharField(max_length=200, null=True, blank=True)),
                ('email', models.CharField(max_length=200, null=True, blank=True)),
                ('services_provided', models.CharField(max_length=200, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('salutation', models.CharField(max_length=5, null=True, verbose_name=b'Salutation', blank=True)),
                ('first_name', models.CharField(max_length=50, null=True, verbose_name=b'First Name', blank=True)),
                ('last_name', models.CharField(max_length=50, null=True, verbose_name=b'Last Name', blank=True)),
                ('position', models.CharField(max_length=50, null=True, verbose_name=b'Position', blank=True)),
                ('phone_number', models.CharField(max_length=25, null=True, verbose_name=b'Phone Number', blank=True)),
                ('fax_number', models.CharField(max_length=25, null=True, verbose_name=b'Fax Number', blank=True)),
                ('cell_number', models.CharField(max_length=25, null=True, verbose_name=b'Cell Number', blank=True)),
                ('contact_email', models.EmailField(max_length=75, null=True, verbose_name=b'Contact E-Mail', blank=True)),
                ('contact_address', models.CharField(max_length=500, null=True, verbose_name=b'Contact Address', blank=True)),
                ('country', models.CharField(max_length=50, null=True, verbose_name=b'Country', blank=True)),
                ('state', models.CharField(max_length=50, null=True, verbose_name=b'State', blank=True)),
                ('city', models.CharField(max_length=50, null=True, verbose_name=b'City', blank=True)),
                ('zip_code', models.CharField(max_length=15, null=True, verbose_name=b'Zip Code', blank=True)),
                ('method_of_notification', models.CharField(max_length=10, null=True, verbose_name=b'Method of Notification', blank=True)),
                ('preferred_password', models.CharField(max_length=128, null=True, verbose_name=b'Password', blank=True)),
                ('subscription_status', models.CharField(max_length=10, null=True, verbose_name=b'Subscription Status', blank=True)),
                ('subscription_date', models.DateField(null=True, blank=True)),
                ('subscription_expire_date', models.DateField(null=True, blank=True)),
                ('profile_completion_status', models.CharField(max_length=10, null=True, verbose_name=b'Profile Completion Status', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SupplierCompany',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comp_name', models.CharField(max_length=200, null=True, verbose_name=b'Legal Company Name', blank=True)),
                ('organization_type', models.CharField(max_length=50, null=True, verbose_name=b'Organization Type', blank=True)),
                ('doing_business_as', models.CharField(max_length=200, null=True, verbose_name=b'DBA Company Name', blank=True)),
                ('tax_id_number', models.CharField(max_length=50, null=True, verbose_name=b'Federal Tax ID', blank=True)),
                ('social_security_number', models.CharField(max_length=50, null=True, verbose_name=b'Social Security Number', blank=True)),
                ('comp_dunn_street', models.CharField(max_length=50, null=True, verbose_name=b'Dunn & Brad Street Number', blank=True)),
                ('comp_phone', models.CharField(max_length=20, null=True, verbose_name=b'Company Phone Number', blank=True)),
                ('comp_fax', models.CharField(max_length=20, null=True, verbose_name=b'Company Fax Number', blank=True)),
                ('comp_url', models.CharField(max_length=100, null=True, verbose_name=b'Company Website (URL)', blank=True)),
                ('corporate_email', models.EmailField(max_length=75, null=True, verbose_name=b'Corporate E-Mail', blank=True)),
                ('year_established', models.DateField(max_length=15, null=True, verbose_name=b'Year Business was Established', blank=True)),
                ('num_of_employees', models.CharField(max_length=10, null=True, verbose_name=b'Number Of Employees', blank=True)),
                ('product_service_description', models.TextField(max_length=200, null=True, verbose_name=b'Product & Service Description', blank=True)),
                ('comp_logo', models.ImageField(upload_to=b'attachment/company/', null=True, verbose_name=b'Current Company Logo', blank=True)),
                ('comp_picture', models.ImageField(upload_to=b'attachment/company/', null=True, verbose_name=b'Current Company/Personal Picture', blank=True)),
                ('capability', models.ForeignKey(blank=True, to='supplier.CompanyCapabilityStatement', null=True)),
                ('comp_address', models.ForeignKey(blank=True, to='supplier.Address', null=True)),
                ('ps_categories', models.ManyToManyField(to='supplier.ProductAndServiceCategory', null=True, blank=True)),
                ('supplier', models.OneToOneField(to='supplier.Supplier')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SupplierSelectedBuyers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('selection_date', models.DateTimeField(auto_now=True, auto_now_add=True, null=True, verbose_name=b'Selection Date')),
                ('submission_date', models.DateTimeField(null=True, verbose_name=b'Submission Date')),
                ('submission_status', models.CharField(blank=True, max_length=10, null=True, verbose_name=b'Submission Status', choices=[(0, b'Profile Not Complate'), (1, b'Pending'), (2, b'Submitted'), (3, b'Error in Submission')])),
                ('buyer', models.ForeignKey(to='supplier.Buyer')),
                ('supplier', models.ForeignKey(to='supplier.Supplier')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='reference',
            name='company',
            field=models.ForeignKey(to='supplier.SupplierCompany'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='companyrevenue',
            name='company',
            field=models.OneToOneField(to='supplier.SupplierCompany'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='companyrevenue',
            name='payment_address',
            field=models.ForeignKey(blank=True, to='supplier.Address', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='companyproductservice',
            name='company',
            field=models.OneToOneField(to='supplier.SupplierCompany'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='companyowner',
            name='company',
            field=models.ForeignKey(to='supplier.SupplierCompany'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='companycontact',
            name='company',
            field=models.ForeignKey(to='supplier.SupplierCompany'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='companycertification',
            name='company',
            field=models.ForeignKey(to='supplier.SupplierCompany'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='buyer',
            name='product_service_category',
            field=models.ManyToManyField(to='supplier.ProductAndServiceCategory', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='buyer',
            name='ps_buy_code',
            field=models.ManyToManyField(related_name='comp_buy_codes', null=True, to='supplier.ProductServiceCode', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='businesscertificate',
            name='company',
            field=models.ForeignKey(to='supplier.SupplierCompany'),
            preserve_default=True,
        ),
    ]
