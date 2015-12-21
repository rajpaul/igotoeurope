# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('supplier', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivationCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=200)),
                ('creation_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('expire_date', models.DateTimeField(default=datetime.datetime(2015, 2, 25, 9, 49, 53, 690522), null=True, blank=True)),
                ('status', models.IntegerField(choices=[(0, b'ACTIVE'), (1, b'USED'), (2, b'INACTIVE'), (3, b'EXPIRED')])),
                ('code_for', models.IntegerField(blank=True, null=True, choices=[(1, b'PASSWORD_RESET'), (0, b'USER_REGISTER')])),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CouponCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=50, unique=True, null=True, blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('expire_date', models.DateTimeField(null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('status', models.CharField(max_length=10, null=True, blank=True)),
                ('discount_amount', models.DecimalField(null=True, max_digits=8, decimal_places=2, blank=True)),
                ('discount_type', models.CharField(blank=True, max_length=2, null=True, choices=[(b'0', b'Fixed'), (b'1', b'Percent')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CouponSupplier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_time', models.DateTimeField(null=True, blank=True)),
                ('coupon', models.ForeignKey(blank=True, to='subscriber.CouponCode', null=True)),
                ('subscriber', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Frequency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('duration_title', models.CharField(blank=True, max_length=50, null=True, choices=[(b'30', b'Monthly Registration'), (b'120', b'Quarterly Registration'), (b'182', b'Half-yearly Registration'), (b'365', b'Yearly Registration')])),
                ('display_order', models.IntegerField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('package_name', models.CharField(max_length=50, null=True, verbose_name=b'Package Name', blank=True)),
                ('display_order', models.IntegerField(null=True, blank=True)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PackagePlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.DecimalField(null=True, max_digits=8, decimal_places=2, blank=True)),
                ('frequency', models.ForeignKey(to='subscriber.Frequency')),
                ('package', models.ForeignKey(to='subscriber.Package')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PaymentHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('plan_amount', models.DecimalField(null=True, max_digits=8, decimal_places=2, blank=True)),
                ('net_amount', models.DecimalField(null=True, max_digits=8, decimal_places=2, blank=True)),
                ('payment_id', models.CharField(max_length=100, null=True, blank=True)),
                ('transaction', models.CharField(max_length=500, null=True, blank=True)),
                ('payment_status', models.CharField(max_length=10, null=True, blank=True)),
                ('create_time', models.DateTimeField(null=True, blank=True)),
                ('token', models.CharField(max_length=100, null=True, blank=True)),
                ('coupon', models.ForeignKey(blank=True, to='subscriber.CouponCode', null=True)),
                ('plan', models.ForeignKey(to='subscriber.PackagePlan')),
                ('supplier', models.ForeignKey(to='supplier.Supplier')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, null=True, verbose_name=b'Service Title', blank=True)),
                ('display_order', models.IntegerField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subscription_date', models.DateTimeField(auto_now_add=True)),
                ('expire_date', models.DateTimeField(null=True, blank=True)),
                ('plan_amount', models.DecimalField(null=True, max_digits=8, decimal_places=2, blank=True)),
                ('net_amount', models.DecimalField(null=True, max_digits=8, decimal_places=2, blank=True)),
                ('subscription_status', models.CharField(max_length=10, null=True, blank=True)),
                ('coupon_used', models.ForeignKey(blank=True, to='subscriber.CouponCode', null=True)),
                ('package_plan', models.ForeignKey(to='subscriber.PackagePlan')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='package',
            name='services',
            field=models.ManyToManyField(to='subscriber.Service'),
            preserve_default=True,
        ),
    ]
