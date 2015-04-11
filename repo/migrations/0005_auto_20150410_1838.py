# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repo', '0004_remove_source_display_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='source',
            name='type',
        ),
        migrations.AddField(
            model_name='source',
            name='measurement_types',
            field=models.ManyToManyField(to='repo.MeasurementType'),
            preserve_default=True,
        ),
    ]
