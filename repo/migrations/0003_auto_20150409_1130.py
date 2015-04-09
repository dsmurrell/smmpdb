# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repo', '0002_source_email_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='source',
            name='source_data',
        ),
        migrations.DeleteModel(
            name='SourceData',
        ),
        migrations.AddField(
            model_name='source',
            name='meta_file',
            field=models.FileField(default='null', upload_to=b'source/%Y/%m/%d'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='source',
            name='smiles_file',
            field=models.FileField(default='null', upload_to=b'source/%Y/%m/%d'),
            preserve_default=False,
        ),
    ]
