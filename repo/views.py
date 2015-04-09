# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from tasks import predict_logp, import_task

import logging
logger = logging.getLogger('repo')

from repo.models import SourceData
from repo.forms import *

from utils import *

from django.conf import settings

def datasets(request):
    sources = Source.objects.all()
    for source in sources:
        print source.name
    return render_to_response(
        'datasets.html',
        {'sources': sources},
        context_instance=RequestContext(request)
    )

def predict(request):
    models = Model.objects.all()
    for model in models:
        print model.type
    return render_to_response(
        'predict.html',
        {'models': models},
        context_instance=RequestContext(request)
    )

def smlogp(request):
    if request.method == 'POST':
        form = MoleculeFileForm(request.POST, request.FILES)
        if form.is_valid():
            molecule_file = MoleculeFile(molecule_file = request.FILES['molecule_file'])
            molecule_file.save()
            molecule_file_path = os.path.join(settings.MEDIA_ROOT, molecule_file.molecule_file.name)
            email_address = form.cleaned_data['email_address']

            predict_logp.delay(molecule_file_path, email_address)

            return render_to_response(
                'smlogp.html',
                {'processing': """LogP prediction in progress........
                                    results will be emailed to you.""", 'show_form': False},
                context_instance=RequestContext(request)
                )
    else:
        form = MoleculeFileForm()
        return render_to_response(
            'smlogp.html',
            {'form': form, 'show_form': True},
            context_instance=RequestContext(request)
        )

def submit(request):
    if request.method == 'POST':
        print "YO MOFO"
        form = SourceDataForm(request.POST, request.FILES)
        if form.is_valid():
            source_data = SourceData(smiles_file = request.FILES['smiles_file'], meta_file = request.FILES['meta_file'])
            source_data.save()

            email_address = form.cleaned_data['email_address']
            display_name = form.cleaned_data['email_address']
            url = form.cleaned_data['url']
            description = form.cleaned_data['description']

            source = Source(email_address = email_address, display_name = display_name, url = url, description = description, source_data = source_data)

            import_task.delay(source_data, email_address)

            return render_to_response(
                'submit.html',
                {'processing': 'Thank you for your submission... if anything unexpected happened you will be contacted.', 'show_form': False},
                context_instance=RequestContext(request)
            )
        else:
            return render_to_response(
                'submit.html',
                {'form': form, 'show_form': True},
                context_instance=RequestContext(request)
            )
    else:
        form = SourceDataForm()
        return render_to_response(
            'submit.html',
            {'form': form, 'show_form': True},
            context_instance=RequestContext(request)
        )

def test(request):
    capture = Capture()
    # make all print statements go to the text field in the capture object
    sys.stdout = capture
    
    # Handle file upload
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            input = form.cleaned_data['input']
            
            if 'print_input' in request.POST:
                print input
                
            if 'delete_source' in request.POST:
                deleteSource(input)
            
            if 'print_compound_duplicates' in request.POST:
                if input != "":
                    printMultipleMeasurementsOfType(input)
                else:
                    printMultipleMeasurements()
                
            if 'print_compound_hanging' in request.POST:
                printNoMeasurements()
                
            if 'dump_multiple_sources' in request.POST:
                dump_multiple_sources(input)
    else:
        form = TestForm() # A empty, unbound form
        
    # reassign the print statements to the terminal 
    sys.stdout = capture.terminal

    # Render test page with the documents and the form
    return render_to_response(
        'test.html',
        {'form': form, 'output': capture.text},
        context_instance=RequestContext(request)
    )