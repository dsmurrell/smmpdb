# daniel@Daniels-MacBook-Air.local:~/Dropbox/projects/propertyDB$ python manage.py inspectdb
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models
import os

class Model(models.Model):
    type = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    class Meta:
        db_table = u'model'
    def __unicode__(self):
        return u'%s: %s' % (self.type, self.description)
    
class MoleculeFile(models.Model):
    molecule_file = models.FileField(upload_to='molecule_file/%Y/%m/%d')
    class Meta:
        db_table = u'molecule_file'
    def __unicode__(self):
        return u'%s' % (os.path.basename(self.molecule_file.name))

class Source(models.Model):
    email_address = models.EmailField(blank=False)
    name = models.CharField(max_length=300, blank=True)
    url = models.CharField(max_length=300, db_column='URL', blank=True)
    type = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    smiles_file = models.FileField(upload_to='source/%Y/%m/%d')
    meta_file = models.FileField(upload_to='source/%Y/%m/%d')
    class Meta:
        db_table = u'source'   
    def __unicode__(self):
        return u'%s' % (self.name)

class Reference(models.Model):
    doi = models.CharField(max_length=135, db_column='DOI', blank=True)
    title = models.CharField(max_length=300, blank=True)
    abstract = models.TextField(blank=True)
    year = models.IntegerField(null=True, blank=True)
    author_list = models.CharField(max_length=135, blank=True)
    class Meta:
        db_table = u'reference'
    def __unicode__(self):
        return u'%s' % (self.doi)
        
class Compound(models.Model):
    smiles = models.CharField(max_length=600, db_column='SMILES', blank=True, db_index=True)
    inchi = models.CharField(max_length=600, db_column='InChI', blank=True)
    inchi_key = models.CharField(max_length=81, db_column='InChI_key', blank=True)
    class Meta:
        db_table = u'compound'
    def __unicode__(self):
        return u'%s' % (self.smiles)

class ConditionType(models.Model):
    type = models.CharField(max_length=135, blank=True)
    description = models.TextField(blank=True)
    class Meta:
        db_table = u'condition_type'

class Condition(models.Model):
    description = models.TextField(blank=True)
    value = models.DecimalField(null=True, max_digits=14, decimal_places=6, blank=True)
    condition_type = models.ForeignKey(ConditionType)
    class Meta:
        db_table = u'condition'
        
class MeasurementType(models.Model):
    type = models.CharField(max_length=135, blank=True)
    description = models.TextField(blank=True)
    class Meta:
        db_table = u'measurement_type'
    def __unicode__(self):
        return u'%s' % (self.type)
        
class MeasurementSet(models.Model):
    trials = models.IntegerField(null=True, blank=True)
    mean = models.DecimalField(null=True, max_digits=14, decimal_places=6, blank=True)
    sd = models.DecimalField(null=True, max_digits=14, decimal_places=6, blank=True)
    open = models.BooleanField(default=False)
    predicted = models.BooleanField(default=False)
    compound = models.ForeignKey(Compound)
    measurement_type = models.ForeignKey(MeasurementType)
    units = models.CharField(max_length=135, blank=True)
    original_format = models.CharField(max_length=600, blank=True)
    original_format_type = models.CharField(max_length=45, blank=True)
    external_id = models.IntegerField(null=True, blank=True)
    source = models.ForeignKey(Source)
    reference = models.ForeignKey(Reference, null=True)
    class Meta:
        db_table = u'measurement_set'
    def __unicode__(self):
        return u'CS:%s OS:%s    %s: %s' % (self.compound.smiles, self.original_format, self.measurement_type.type, self.mean)

class ConditionHasMeasurementSet(models.Model):
    condition = models.ForeignKey(Condition)
    measurement_set = models.ForeignKey(MeasurementSet)
    class Meta:
        db_table = u'condition_has_measurement_set' 

class Measurement(models.Model):
    value = models.DecimalField(null=True, max_digits=14, decimal_places=6, blank=True)
    measurement_set = models.ForeignKey(MeasurementSet)
    class Meta:
        db_table = u'measurement'
    def __unicode__(self):
        return u'%s: %s' % (self.measurement_set.compound.smiles, self.value)
