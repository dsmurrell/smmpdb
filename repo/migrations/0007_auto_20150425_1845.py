# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repo', '0006_auto_20150410_1904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measurementset',
            name='external_id',
            field=models.CharField(max_length=30),
            preserve_default=True,
        ),
    ]
