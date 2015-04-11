# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repo', '0005_auto_20150410_1838'),
    ]

    operations = [
        migrations.AddField(
            model_name='measurementtype',
            name='sources',
            field=models.ManyToManyField(to='repo.Source', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='source',
            name='measurement_types',
            field=models.ManyToManyField(to='repo.MeasurementType', blank=True),
            preserve_default=True,
        ),
    ]
