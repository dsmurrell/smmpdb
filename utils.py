import sys, csv
from repo.models import *
from django.conf import settings

from indigo.indigo import *
from myindigo import MyIndigo
indigo = Indigo()

class Capture(object):
        def __init__(self):
            self.terminal = sys.stdout
            self.text = ''

        def write(self, message):
            # does this capture write to the terminal too?
            #self.terminal.write(message) 
            self.text += message

def findHooks(source_name, measurement_type_type, reference_name) :
    qs = Source.objects.filter(name=source_name)
    if qs.count() == 0:
        print "Source \'" + source_name + "\' does not exist in database."
        sys.exit()
    source = qs[0]
        
    qs = MeasurementType.objects.filter(type=measurement_type_type)
    if qs.count() == 0:
        print "MeasurementType \'" + measurement_type_type + "\' does not exist in database."
        sys.exit()
    measurement_type = qs[0]
        
    qs = Reference.objects.filter(name=reference_name)
    if qs.count() == 0:
        print "Reference \'" + reference_name + "\' does not exist in database."
        sys.exit()
    reference = qs[0]
        
    return source, measurement_type, reference
    
# delete all entries associated with a source
def deleteSource(source_name):
    print "deleting objects associated with source: " + source_name
    measurements = Measurement.objects.filter(measurement_set__source__name__exact=source_name)
    measurements.delete()
    measurement_sets = MeasurementSet.objects.filter(source__name__exact=source_name)
    measurement_sets.delete()
    print "done deleting objects"
    deleteNoMeasurements()
    print "deleting compounds with no measurements"
    
# delete reference entries associated with a source
def removeReferenceFromSource(source_name, reference):
    print "removing references from objects associated with source: " + source_name
    measurement_sets = MeasurementSet.objects.filter(source__name__exact=source_name)
    for measurement_set in measurement_sets:
        measurement_set.reference = reference
        measurement_set.save()
    print "done removing references"
    
# prints all the information about compounds that contain more than one measurement in the database
def printMultipleMeasurements():
    compounds = Compound.objects.all()
    for compound in compounds:
        qs = MeasurementSet.objects.filter(compound=compound)
        if qs.count() > 1:
            print "Multiple Measurements"
            for i in range(0,qs.count()):
                print qs[i].source.name + ': ' + qs[i].original_format + ' ' + str(qs[i].mean)
            print ''
            
def printMultipleMeasurementsOfType(type):
    compounds = Compound.objects.all()
    for compound in compounds:
        qs = MeasurementSet.objects.filter(compound=compound, measurement_type__type = type)
        if qs.count() > 1:
            print "Multiple Measurements"
            for i in range(0,qs.count()):
                print qs[i].source.name + ': ' + qs[i].original_format + ' ' + str(qs[i].mean)
            print ''
            
# delete all the compounds, sources, references and measurement types with no measurements
def deleteNoMeasurements():
    compounds = Compound.objects.all()
    for compound in compounds:
        qs = MeasurementSet.objects.filter(compound=compound)
        if qs.count() == 0:
            compound.delete()
            
    sources = Source.objects.all()
    for source in sources:
        qs = MeasurementSet.objects.filter(source=source)
        if qs.count() == 0:
            if hasattr(source,'source_data'):
                source.source_data.smiles_file.delete()
                source.source_data.meta_file.delete()
                source.source_data.delete()
            source.delete()
            
    measurement_types = MeasurementType.objects.all()
    for measurement_type in measurement_types:
        qs = MeasurementSet.objects.filter(measurement_type=measurement_type)
        if qs.count() == 0:
            measurement_type.delete()
            
    references = Reference.objects.all()
    for reference in references:
        qs = MeasurementSet.objects.filter(reference=reference)
        if qs.count() == 0:
            reference.delete()
            
# prints all the compounds with no measurements
def printNoMeasurements():
    count = 0
    compounds = Compound.objects.all()
    for compound in compounds:
        qs = MeasurementSet.objects.filter(compound=compound)
        if qs.count() == 0:
            print compound.smiles
            count = count+1
    print count
            
def dump_multiple_sources(input):
    print os.getcwd()
    structures_file = open('structures.smi', 'w') 
    structures_writer = csv.writer(structures_file, delimiter = '\t')
    
    targets_file = open('targets.csv', 'w') 
    targets_writer = csv.writer(targets_file, delimiter = ',')
    
    compounds = Compound.objects.all()
    for compound in compounds:
        qs = MeasurementSet.objects.filter(compound=compound)
        value = 0
        for i in range(1,qs.count()):
            value = value + qs[i].mean
        value = round(value / qs.count())
        structures_writer.writerow([compound.smiles] + [compound.id])
        targets_writer.writerow([compound.id] + [value])
        
    print os.getcwd()
    
# adds a single measurement entry to the database
def addSingleMeasurement(external_id,
                         canonical_smiles,
                         original_format,
                         original_format_type,
                         value,
                         units,
                         is_open,
                         is_predicted,
                         source,
                         measurement_type,
                         reference):
    # get or create compound   
    compound, created = Compound.objects.get_or_create(smiles=canonical_smiles)
    open_boolean = is_open=="TRUE"
    predicted_boolean = is_predicted=="TRUE"
    # add measurement_set   
    measurement_set = MeasurementSet(trials = 1,
                                     mean = value,
                                     sd = -1,
                                     open = open_boolean,
                                     predicted = predicted_boolean,
                                     compound = compound,
                                     measurement_type = measurement_type,
                                     units = units,
                                     original_format = original_format,
                                     original_format_type = original_format_type,
                                     external_id = external_id,
                                     source = source,
                                     reference = reference)
    measurement_set.save()
    # add measurement
    measurement = Measurement(value = value, measurement_set = measurement_set)
    measurement.save()
    
# import data from entry template
def importFromSourceData(source_data):
    smiles_file = os.path.join(settings.MEDIA_ROOT, source_data.smiles_file.name)
    meta_file = os.path.join(settings.MEDIA_ROOT, source_data.meta_file.name)
    
    mi = MyIndigo.MyIndigo(indigo)
    molecules = mi.readSmiles(smiles_file)
    d = {}
    with open(meta_file, 'rb') as csvfile:
         r = csv.reader(csvfile, delimiter=',', quotechar='"')
         header = r.next()
         print header
         for row in r:
            d[row[0]] = row
    
    for molecule in molecules:
        external_id = molecule.name()
        row = d[external_id]
        
        original_format = row[1]
        original_format_type = row[2]
        value = row[3]
        units = row[4]
        source_name = row[5]
        measurement_type_type = row[6]
        reference_name = row[7]
        is_open = row[8]
        is_predicted = row[9]
        
        source, created = Source.objects.get_or_create(name=source_name, source_data = source_data)
        #source.source_data = source_data
        source.save()
        measurement_type, created = MeasurementType.objects.get_or_create(type=measurement_type_type)
        reference, created = Reference.objects.get_or_create(name=reference_name)
        
        molecule.aromatize()
        canonical_smiles = molecule.canonicalSmiles()
        addSingleMeasurement(external_id = external_id,
                             canonical_smiles = canonical_smiles,
                             original_format = original_format,
                             original_format_type = original_format_type,
                             value = value,
                             units = units,
                             is_open = is_open,
                             is_predicted = is_predicted,
                             source = source,
                             measurement_type = measurement_type,
                             reference = reference)