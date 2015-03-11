# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from tasks import predict_logp

import logging
logger = logging.getLogger('repo')

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
import subprocess

from repo.models import SourceData, MoleculeFile
from repo.forms import *

from utils import *

from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMessage

def submit(request):
    capture = Capture()
    # make all print statements go to the text field in the capture object
    sys.stdout = capture
    
    # Handle file upload
    if request.method == 'POST':
        form = SourceDataForm(request.POST, request.FILES)
        if form.is_valid():
            source_data = SourceData(smiles_file = request.FILES['smiles_file'], meta_file = request.FILES['meta_file'])
            source_data.save()
            
            print source_data.smiles_file
            print source_data.meta_file
            
            importFromSourceData(source_data)

            # Redirect to the document submit after POST
            #return HttpResponseRedirect(reverse('repo.views.submit'))
    else:
        form = SourceDataForm() # A empty, unbound form
        
    # reassign the print statements to the terminal 
    sys.stdout = capture.terminal

    # Render sumbit page with the documents and the form
    return render_to_response(
        'submit.html',
        {'form': form, 'output': capture.text},
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
        logger.debug("this is a debug message!")
        form = MoleculeFileForm()
        return render_to_response(
            'smlogp.html',
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