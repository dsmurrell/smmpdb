# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repo', '0003_auto_20150409_1130'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='source',
            name='display_name',
        ),
    ]
