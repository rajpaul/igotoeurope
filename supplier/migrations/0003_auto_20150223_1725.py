# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0002_auto_20150223_1013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companycertification',
            name='certificate_name',
            field=models.OneToOneField(related_name='company_cert', to='supplier.CertificateName'),
            preserve_default=True,
        ),
    ]
