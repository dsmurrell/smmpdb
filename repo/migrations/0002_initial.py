# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SourceData'
        db.create_table(u'source_data', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('smiles_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('meta_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('repo', ['SourceData'])

        # Adding model 'Source'
        db.create_table(u'source', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('display_name', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=300, db_column='URL', blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('source_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repo.SourceData'])),
        ))
        db.send_create_signal('repo', ['Source'])

        # Adding model 'Reference'
        db.create_table(u'reference', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=135, db_column='name', blank=True)),
            ('doi', self.gf('django.db.models.fields.CharField')(max_length=135, db_column='DOI', blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('abstract', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('year', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('author_list', self.gf('django.db.models.fields.CharField')(max_length=135, blank=True)),
        ))
        db.send_create_signal('repo', ['Reference'])

        # Adding model 'Compound'
        db.create_table(u'compound', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('smiles', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=600, db_column='SMILES', blank=True)),
            ('inchi', self.gf('django.db.models.fields.CharField')(max_length=600, db_column='InChI', blank=True)),
            ('inchi_key', self.gf('django.db.models.fields.CharField')(max_length=81, db_column='InChI_key', blank=True)),
        ))
        db.send_create_signal('repo', ['Compound'])

        # Adding model 'ConditionType'
        db.create_table(u'condition_type', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=135, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('repo', ['ConditionType'])

        # Adding model 'Condition'
        db.create_table(u'condition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('value', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=14, decimal_places=6, blank=True)),
            ('condition_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repo.ConditionType'])),
        ))
        db.send_create_signal('repo', ['Condition'])

        # Adding model 'MeasurementType'
        db.create_table(u'measurement_type', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=135, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('repo', ['MeasurementType'])

        # Adding model 'MeasurementSet'
        db.create_table(u'measurement_set', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trials', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('mean', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=14, decimal_places=6, blank=True)),
            ('sd', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=14, decimal_places=6, blank=True)),
            ('open', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('predicted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('compound', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repo.Compound'])),
            ('measurement_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repo.MeasurementType'])),
            ('units', self.gf('django.db.models.fields.CharField')(max_length=135, blank=True)),
            ('original_format', self.gf('django.db.models.fields.CharField')(max_length=600, blank=True)),
            ('original_format_type', self.gf('django.db.models.fields.CharField')(max_length=45, blank=True)),
            ('external_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repo.Source'])),
            ('reference', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repo.Reference'], null=True)),
        ))
        db.send_create_signal('repo', ['MeasurementSet'])

        # Adding model 'ConditionHasMeasurementSet'
        db.create_table(u'condition_has_measurement_set', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('condition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repo.Condition'])),
            ('measurement_set', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repo.MeasurementSet'])),
        ))
        db.send_create_signal('repo', ['ConditionHasMeasurementSet'])

        # Adding model 'Measurement'
        db.create_table(u'measurement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=14, decimal_places=6, blank=True)),
            ('measurement_set', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repo.MeasurementSet'])),
        ))
        db.send_create_signal('repo', ['Measurement'])


    def backwards(self, orm):
        # Deleting model 'SourceData'
        db.delete_table(u'source_data')

        # Deleting model 'Source'
        db.delete_table(u'source')

        # Deleting model 'Reference'
        db.delete_table(u'reference')

        # Deleting model 'Compound'
        db.delete_table(u'compound')

        # Deleting model 'ConditionType'
        db.delete_table(u'condition_type')

        # Deleting model 'Condition'
        db.delete_table(u'condition')

        # Deleting model 'MeasurementType'
        db.delete_table(u'measurement_type')

        # Deleting model 'MeasurementSet'
        db.delete_table(u'measurement_set')

        # Deleting model 'ConditionHasMeasurementSet'
        db.delete_table(u'condition_has_measurement_set')

        # Deleting model 'Measurement'
        db.delete_table(u'measurement')


    models = {
        'repo.compound': {
            'Meta': {'object_name': 'Compound', 'db_table': "u'compound'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inchi': ('django.db.models.fields.CharField', [], {'max_length': '600', 'db_column': "'InChI'", 'blank': 'True'}),
            'inchi_key': ('django.db.models.fields.CharField', [], {'max_length': '81', 'db_column': "'InChI_key'", 'blank': 'True'}),
            'smiles': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '600', 'db_column': "'SMILES'", 'blank': 'True'})
        },
        'repo.condition': {
            'Meta': {'object_name': 'Condition', 'db_table': "u'condition'"},
            'condition_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repo.ConditionType']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '14', 'decimal_places': '6', 'blank': 'True'})
        },
        'repo.conditionhasmeasurementset': {
            'Meta': {'object_name': 'ConditionHasMeasurementSet', 'db_table': "u'condition_has_measurement_set'"},
            'condition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repo.Condition']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'measurement_set': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repo.MeasurementSet']"})
        },
        'repo.conditiontype': {
            'Meta': {'object_name': 'ConditionType', 'db_table': "u'condition_type'"},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '135', 'blank': 'True'})
        },
        'repo.measurement': {
            'Meta': {'object_name': 'Measurement', 'db_table': "u'measurement'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'measurement_set': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repo.MeasurementSet']"}),
            'value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '14', 'decimal_places': '6', 'blank': 'True'})
        },
        'repo.measurementset': {
            'Meta': {'object_name': 'MeasurementSet', 'db_table': "u'measurement_set'"},
            'compound': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repo.Compound']"}),
            'external_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mean': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '14', 'decimal_places': '6', 'blank': 'True'}),
            'measurement_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repo.MeasurementType']"}),
            'open': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'original_format': ('django.db.models.fields.CharField', [], {'max_length': '600', 'blank': 'True'}),
            'original_format_type': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'}),
            'predicted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reference': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repo.Reference']", 'null': 'True'}),
            'sd': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '14', 'decimal_places': '6', 'blank': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repo.Source']"}),
            'trials': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'units': ('django.db.models.fields.CharField', [], {'max_length': '135', 'blank': 'True'})
        },
        'repo.measurementtype': {
            'Meta': {'object_name': 'MeasurementType', 'db_table': "u'measurement_type'"},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '135', 'blank': 'True'})
        },
        'repo.reference': {
            'Meta': {'object_name': 'Reference', 'db_table': "u'reference'"},
            'abstract': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'author_list': ('django.db.models.fields.CharField', [], {'max_length': '135', 'blank': 'True'}),
            'doi': ('django.db.models.fields.CharField', [], {'max_length': '135', 'db_column': "'DOI'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '135', 'db_column': "'name'", 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'repo.source': {
            'Meta': {'object_name': 'Source', 'db_table': "u'source'"},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'source_data': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repo.SourceData']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '300', 'db_column': "'URL'", 'blank': 'True'})
        },
        'repo.sourcedata': {
            'Meta': {'object_name': 'SourceData', 'db_table': "u'source_data'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'smiles_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['repo']