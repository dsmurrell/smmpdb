# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='source',
            name='email_address',
            field=models.EmailField(default='dsmurrell@gmail.com', max_length=75),
            preserve_default=False,
        ),
    ]
