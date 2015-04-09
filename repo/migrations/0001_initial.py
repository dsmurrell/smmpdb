# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Compound',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('smiles', models.CharField(db_index=True, max_length=600, db_column=b'SMILES', blank=True)),
                ('inchi', models.CharField(max_length=600, db_column=b'InChI', blank=True)),
                ('inchi_key', models.CharField(max_length=81, db_column=b'InChI_key', blank=True)),
            ],
            options={
                'db_table': 'compound',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(blank=True)),
                ('value', models.DecimalField(null=True, max_digits=14, decimal_places=6, blank=True)),
            ],
            options={
                'db_table': 'condition',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ConditionHasMeasurementSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('condition', models.ForeignKey(to='repo.Condition')),
            ],
            options={
                'db_table': 'condition_has_measurement_set',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ConditionType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=135, blank=True)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'db_table': 'condition_type',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.DecimalField(null=True, max_digits=14, decimal_places=6, blank=True)),
            ],
            options={
                'db_table': 'measurement',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MeasurementSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('trials', models.IntegerField(null=True, blank=True)),
                ('mean', models.DecimalField(null=True, max_digits=14, decimal_places=6, blank=True)),
                ('sd', models.DecimalField(null=True, max_digits=14, decimal_places=6, blank=True)),
                ('open', models.BooleanField(default=False)),
                ('predicted', models.BooleanField(default=False)),
                ('units', models.CharField(max_length=135, blank=True)),
                ('original_format', models.CharField(max_length=600, blank=True)),
                ('original_format_type', models.CharField(max_length=45, blank=True)),
                ('external_id', models.IntegerField(null=True, blank=True)),
                ('compound', models.ForeignKey(to='repo.Compound')),
            ],
            options={
                'db_table': 'measurement_set',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MeasurementType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=135, blank=True)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'db_table': 'measurement_type',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=300, blank=True)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'db_table': 'model',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MoleculeFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('molecule_file', models.FileField(upload_to=b'molecule_file/%Y/%m/%d')),
            ],
            options={
                'db_table': 'molecule_file',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('doi', models.CharField(max_length=135, db_column=b'DOI', blank=True)),
                ('title', models.CharField(max_length=300, blank=True)),
                ('abstract', models.TextField(blank=True)),
                ('year', models.IntegerField(null=True, blank=True)),
                ('author_list', models.CharField(max_length=135, blank=True)),
            ],
            options={
                'db_table': 'reference',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=300, blank=True)),
                ('display_name', models.CharField(max_length=300, blank=True)),
                ('url', models.CharField(max_length=300, db_column=b'URL', blank=True)),
                ('type', models.CharField(max_length=300, blank=True)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'db_table': 'source',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SourceData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('smiles_file', models.FileField(upload_to=b'source_data/%Y/%m/%d')),
                ('meta_file', models.FileField(upload_to=b'source_data/%Y/%m/%d')),
            ],
            options={
                'db_table': 'source_data',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='source',
            name='source_data',
            field=models.ForeignKey(to='repo.SourceData'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='measurementset',
            name='measurement_type',
            field=models.ForeignKey(to='repo.MeasurementType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='measurementset',
            name='reference',
            field=models.ForeignKey(to='repo.Reference', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='measurementset',
            name='source',
            field=models.ForeignKey(to='repo.Source'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='measurement',
            name='measurement_set',
            field=models.ForeignKey(to='repo.MeasurementSet'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='conditionhasmeasurementset',
            name='measurement_set',
            field=models.ForeignKey(to='repo.MeasurementSet'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='condition',
            name='condition_type',
            field=models.ForeignKey(to='repo.ConditionType'),
            preserve_default=True,
        ),
    ]
